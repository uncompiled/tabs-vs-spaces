import json
import os
import sys
import subprocess
import indent_finder


class Repo:
    def __init__(self, lang, name, clone_url):
        self.language = lang
        self.name = name
        self.clone_url = clone_url

    def process(self):
        """
        Processes the repo and returns whether the majority of the source code files use spaces or tabs.
        :return: string containing spaces or tabs
        """
        # Fetch the git repo
        git_clone_cmd = "git clone -q --depth=1 {} {}".format(self.clone_url, self.name).split(" ")
        subprocess.call(git_clone_cmd)
        # Process the repo for tabs vs. spaces.
        indentation_type = self.__process_files()
        # Clean up working folder.
        subprocess.call(["rm", "-fr", self.name])
        return indentation_type

    def __process_files(self):
        """
        process the files inside the repo
        :return: string containing the indentation style
        """
        repo_style = {
            'tab': 0,
            'space': 0,
            'mixed': 0,
            'unknown': 0
        }

        repo_files = {}
        for root, directories, filenames in os.walk(self.name):
            for filename in filenames:
                if self.__parse_filter(filename):
                    indent_type, indent_amount = indent_finder.parse_file(os.path.join(root, filename),
                                                                          default_tab_width=4,
                                                                          default_result=('unknown', 0))
                    repo_files[os.path.join(root, filename)] = indent_type
                    repo_style[indent_type] += 1

        most_common_style = max(repo_style.keys(), key=(lambda key: repo_style[key]))
        print(self.name, most_common_style, repo_style)
        return most_common_style

    @staticmethod
    def __parse_filter(filename):
        """
        serves as a filter for whether the file should be parsed.
        :param filename: file that should be parsed
        :return: boolean whether the file should be parsed or not.
        """
        filter_rules = ('.go', '.java', '.js', '.php', '.rb', '.py', '.cpp', '.c', '.h')
        # Some repos can use multiple file types, but GitHub classifies the language
        # based on the majority of the codebase, so whitelist the following extensions.
        if filename.endswith(filter_rules):
            return True
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Missing parameter: missing input file.")
    elif len(sys.argv) != 3:
        raise Exception("Missing parameter: missing output file.")

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file) as top_repos:
        repo_data = json.load(top_repos)

        for language, repo_list in repo_data.items():
            for index, repo in enumerate(repo_list):
                # Process the repo and save the indentation type.
                repo['indentation_type'] = Repo(language, repo['name'], repo['clone_url']).process()

        # Write out the results into a new JSON file.
        with open(output_file, 'w') as output:
            output.write(json.dumps(repo_data))
