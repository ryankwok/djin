import os
import re
import subprocess
import traceback
import warnings
from datetime import datetime

import ollama

test_dir_path = ".\\Tests"
specimen_dir_path = ".\\Specimens"
history_dir_path = ".\\History"
design_dir_path = ".\\Designs"


def query_llm(query_text, role='user'):
    # 'role': 'user' - Represents the input from the user or external source.
    # 'role': 'assistant' - Corresponds to the model’s responses.
    # 'role': 'system' - Sets the assistant’s behavior, tone, or personality.
    messages = [{'role': 'system',
                 'content': 'You MUST respond ONLY in python-runnable code and comments. Comment your thought process. I will attempt to run what you send me.'},
                {'role': role, 'content': query_text}]
    response = ollama.chat(model='llama3', messages=messages)
    return response


def process_user_input():
    user_input = []
    while True:
        line = input()
        if not line:
            break
        user_input.append(line)
    return '\n'.join(user_input)


def write_to_file(file_path, payload):
    if not os.path.exists(os.path.dirname(file_path)):
        os.mkdir(os.path.dirname(file_path))
    f = open(file_path, "w")
    f.write(payload)
    f.close()


def revise_through_crash_report():
    """
    Sends the crash report back to the LLM, gets the updated code and tries again
    """
    max_tries = 5
    for i in range(max_tries):
        query_llm("This was the code you provided: {}\nAnd returned the following error: {}\n\nPlease re-write your entry and resubmit it.".format())


def sanitize_python(raw_response):
    """
    Takes in a raw query and formats it in a way that is hopefully runnable
    """
    processed = raw_response.replace('```', '')
    processed = processed.replace('"""', "'''")
    processed = re.sub(r'\s+python\s+', ' ', processed)
    return processed


def run_subprocess(list_of_command_and_args):
    # try to run the unit test for the script
    exception_str = ''
    try:
        subprocess.run(list_of_command_and_args, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Subprocess failed with return code {e.returncode}: {e.stderr}")
        print(' '.join(list_of_command_and_args))
        traceback.print_exc()
        exception_str = e.stderr
    # Then return the result of the LLM query
    return exception_str


def comment_out(text):
    """ createa commented-out version of original text """
    return text.replace('\n', '\n# ')


def attach_header(file_content, query_used):
    return "# Generated at {}\n# Query:\n# {}\n#\n# {}".format(datetime.now(),
                                                               comment_out(query_used),
                                                               file_content)


def generate_unit_test(topic, context):
    imports = "from Specimens.{} import *".format(topic)
    query = "Please write a series of unit tests using pytest that would be typical of code meetinb the following requirements:\n{}\ninclude this import at the top:\n{}".format(context, imports)
    print("Q: {}".format(query))
    response_datagram = query_llm(query)
    response = response_datagram['message']['content']
    print("A: {}".format(response))
    latest_test_path = test_dir_path + '\\' + topic + '_test.py'
    processed_code = sanitize_python(response)
    file_contents = attach_header(processed_code, query)
    write_to_file(latest_test_path, file_contents)
    return latest_test_path


def generate_and_test_specimen(topic, query, iteration):
    print("Q: {}".format(query))
    response_datagram = query_llm(query)
    response = response_datagram['message']['content']
    print("A: {}".format(response))
    latest_specimen_path = specimen_dir_path + '\\' + topic + '.py'
    latest_history_path = history_dir_path + '\\' + topic + '\\' + topic + '_' + str(iteration) + '.py'
    latest_test_path = test_dir_path + '\\' + topic + '_test.py'
    processed_code = sanitize_python(response)
    file_contents = attach_header(processed_code, query)
    write_to_file(latest_specimen_path, file_contents)
    # in addition to saving the current specimen, save each iteration in the history subfolder
    write_to_file(latest_history_path, file_contents)

    # try to run the generated python script to see if it crashes
    exception_str = run_subprocess(["python", latest_specimen_path])
    exception_str = sanitize_python(exception_str)
    # if the script crashes, send output back to use in follwwup query
    if not is_test_passed(exception_str):
        return response, exception_str

    # try to run the unit test for the script, testing functionality
    start_stamp = datetime.now()
    exception_str = run_subprocess(["pytest", latest_test_path])
    execution_time = datetime.now() - start_stamp
    print("Test {} finished in {} ms".format(latest_test_path, execution_time))
    return response, exception_str


def is_test_passed(exception_str):
    """ Just to make the code easier to read """
    return bool(exception_str == '')


def sanitize_input(raw_in):
    processed = raw_in.strip().lower()
    return processed


def create_specimen_from_unit_test(basename, max_tries, functions_to_generate=[]):
    """ returns a path to the created script, or None if the process failed """
    test_path = test_dir_path + '\\' + basename + "_test.py"
    try:
        unit_test_file = open(test_path, "r")
    except FileNotFoundError:
        print("Could not test find file at: {}. Generating new test...".format(test_path))
        return None
    unit_text_text = unit_test_file.read()
    import_suffix = '*'
    if not functions_to_generate:
        import_suffix = ', '.join(functions_to_generate)
    import_str = "import pytest\nfrom Specimens.{} import {}".format(basename, import_suffix)
    query_str = "Provide the contents of {}.py that satisfies the following pytest unit test:\n\n{}\n{}".format(basename, import_str, unit_text_text)
    print(query_str)
    # Send to the LLM, generate some code, and try to run it. Returns the result
    generated_code_str, exception_str = generate_and_test_specimen(basename, query_str, 0)

    # While the code fails to run, regenerate it with a different prompt
    tries = 1
    while not is_test_passed(exception_str):
        # you can set max_tries to -1 to unlimited tries
        loop_retry_until_success = max_tries <= -1
        if tries >= max_tries and not loop_retry_until_success:
            raise TimeoutError("Timeout occurred after {} tries on exception: {}".format(tries, exception_str))

        # Until there are no problems running the auto-generated code, regenerate it
        query_str = "There was a problem running the code: {}\n\nThe `error was: {}\n\nPlease try again".format(generated_code_str, exception_str)
        print(query_str)
        generated_code_str, exception_str = generate_and_test_specimen(basename, query_str, tries)
        tries += 1
    print("Got it running in {} tries!".format(tries))
    return specimen_dir_path


# TODO: Add mass specimeen creation, \
#  file system awareness, modifiers, evlutionary algo
def main():
    basename = sanitize_input(input('Please enter a basename:'))
    specimen_dir = create_specimen_from_unit_test(basename, 1000)
    if specimen_dir is not None:
        print("Opening generated specimen: {}".format(specimen_dir))
        subprocess.Popen('explorer "{}"'.format(specimen_dir))
        close_app()
    # if the name doesnt exist, assume they want to generate a test
    context = sanitize_input(input('Please provide a description of the code to be written:'))
    generated_test_filepath = generate_unit_test(basename, context)
    if generated_test_filepath is not None:
        print("Opening generated test: {}".format(generated_test_filepath))
        subprocess.Popen('explorer "{}"'.format(generated_test_filepath))
        close_app()


def close_app():
    print("Wish granted")
    quit()


if __name__ == "__main__":
    main()
