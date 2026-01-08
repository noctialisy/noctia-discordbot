import os, sys, json, shutil


def main():
    commands = sys.argv

    if len(commands) <= 1:
        print('No command specified.')
        print('')

    else:
        with open('./settings.json', 'r', encoding='utf-8') as settings_file:
            settings = json.load(settings_file)

            for command in commands:
                if command == "build":
                    deploy_path = settings["k8s.deploy.path"]
                    container_image = settings["k8s.container.image"]
                    img_pull_sec = settings["k8s.container.image.secret"]

                    shutil.copy2('./k8s_noctiabot_example.yaml', 'k8s_noctiabot.yaml')
                    filedata = ""
                    with open('k8s_noctiabot.yaml', 'r', encoding='utf-8') as file:
                        filedata = file.read()
                        filedata = filedata.replace('${k8s.deploy.path}', deploy_path)
                        filedata = filedata.replace('${k8s.container.image}', container_image)
                        filedata = filedata.replace('${k8s.container.image.secret}', img_pull_sec)

                    with open('k8s_noctiabot.yaml', 'w', encoding='utf-8') as file:
                        file.write(filedata)

main()


