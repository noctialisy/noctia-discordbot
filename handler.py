import os, sys, json, shutil, subprocess


def main():
    commands = sys.argv

    if len(commands) <= 1:
        print('No command specified.')
        print('')

    else:
        with open('./settings.json', 'r', encoding='utf-8') as settings_file:
            settings = json.load(settings_file)

            for command in commands:
                if command == "delete":
                    subprocess.run('kubectl delete -f ./k8s_noctiabot.yaml')
                    exit()

                if command == "apply":
                    subprocess.run('kubectl apply -f ./k8s_noctiabot.yaml')
                    exit()
                
                if command == "build":
                    shutil.copy2('./kubernetes.yaml', 'k8s_noctiabot.yaml')
                    filedata = ""

                    with open('k8s_noctiabot.yaml', 'r', encoding='utf-8') as file:
                        filedata = file.read()

                        for key, value in settings.items():
                            filedata = filedata.replace('${'+key+'}', str(value))

                    with open('k8s_noctiabot.yaml', 'w', encoding='utf-8') as file:
                        file.write(filedata)

                    exit()

main()


