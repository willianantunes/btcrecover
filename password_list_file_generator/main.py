import subprocess

from pathlib import Path

from password_list_file_generator.utils import create_structure

subprocess_params = {"capture_output": True, "encoding": "utf8", "shell": True}
command_generate_password = "python btcrecover.py --dsw --listpass --tokenlist {origin} >> {target}"

token_combinations = {
    "1_wig": "%[wW]%1,2[iI]g",
    "2_wig": "%2,3[w]%1,3[iI]%3,6[g]",
    "1_bald": "b%[aA@]ld",
}


def handle():
    print("Gathering required files...")
    btc_recover_file = Path("../btcrecover.py").resolve()
    assert btc_recover_file.exists(), "btcrecover.py not found"
    where_btc_recover_is = btc_recover_file.parent
    subprocess_params["cwd"] = where_btc_recover_is
    password_list_file = Path("password_list.txt").resolve()

    print("Generating password list file...")
    with create_structure(token_combinations) as (current_folder, created_files):
        total_files = len(created_files)
        for index, token_list in enumerate(created_files, start=1):
            print(f"Generating password list file {index} of {total_files}...")
            command = command_generate_password.format(origin=token_list, target=password_list_file)
            process_run = subprocess.run(command, **subprocess_params)
            if process_run.returncode != 0:
                print(f"Error generating password list file")
                print(process_run.stderr)
                print(process_run.stdout)

    print(f"Enriching {password_list_file}...")
    # TODO


if __name__ == "__main__":
    handle()
    print("Done!")
