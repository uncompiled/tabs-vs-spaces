import json
import sys

if __name__ == "__main__":
    # Run this to programmatically summarize the data into a JSON object.
    if len(sys.argv) < 2:
        raise Exception("Missing parameter: missing input file.")
    elif len(sys.argv) != 3:
        raise Exception("Missing parameter: missing output file.")

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file) as top_repos:
        repo_data = json.load(top_repos)
        aggregation = {}

        for language, repo_list in repo_data.items():
            aggregation[language] = {
                'tab': 0,
                'space': 0,
                'mixed': 0,
                'unknown': 0
            }
            for index, repo in enumerate(repo_list):
                aggregation[language][repo["indentation_type"]] += 1

        # Write out the results into a new JSON file.
        with open(output_file, 'w') as output:
            output.write(json.dumps(aggregation))
