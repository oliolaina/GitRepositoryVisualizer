import os
import zlib
import sys
import struct
from datetime import datetime

#аргументы по умолчанию
program = 'plantuml'
repo_path = '../.venv/project_3'
result_file = 'result.txt'
date = '2024-11-29'

if (len(sys.argv) >= 3):
    repo_path = sys.argv[1]
if (len(sys.argv) >= 4):
    if os.path.exists(sys.argv[2]) == 0:
        errorargs()
    codefile = sys.argv[2]
if (len(sys.argv) >= 5):
    if os.path.exists(sys.argv[3]) == 0:
        errorargs()
    data = sys.argv[3]

class GitVisualizer:
    def __init__(self, repo_path, date):
        self.repo_path = repo_path #путь к репозиторию
        self.commits = {}
        self.blobs = []
        self.date = date

    #читает объекты из папки .git/objects и расшифровывает их содержимое
    def read_object(self, sha):
        # создание пути к объекту в файловой системе
        object_path = (self.repo_path + '/.git/objects/' + sha[:2] + '/' + sha[2:])

        with open(object_path, 'rb') as f:
            decompressed_data = f.read()

        #print(object_path)
        #print(decompressed_data)
        # Декомпрессия
        decompressed_data = zlib.decompress(decompressed_data)

        # Получение типа объекта и его содержимого
        header_end = decompressed_data.find(0)
        header = decompressed_data[:header_end]

        content = decompressed_data[header_end+1:]
        stroka = content.decode().split('\n')
        time = stroka[-4].split()
        time = datetime.utcfromtimestamp(int(time[-2])).strftime('%Y-%m-%d %H:%M:%S')
        day = time.split()[0]
        #print(day, date)
        #print(type(content) == bytes)
        if (day < self.date):
            #print(day, date)
            return content.decode()

        return content


    def read_object_tree(self, sha):
        object_path = (self.repo_path + '/.git/objects/' + sha[:2] + '/' + sha[2:])

        with open(object_path, 'rb') as f:
            compressed_data = f.read()
        data = zlib.decompress(compressed_data)
        header, data = data.split(b' ', 1)
        size, data = data.split(b'\x00', 1)

        header = header.decode()
        size = int(size)

        while(data):
            mode, data = data.split(b' ', 1)
            name, data = data.split(b'\x00', 1)
            h, data = data[:20], data[20:]
            #print(mode, name, h)

            #if not {'parent': sha, 'name': name.decode(), 'hash': h.hex()} == self.blobs[sha]:
            self.blobs.append({
                'parent': sha,
                'name': name.decode(),
                'blob' : h.hex()
            })

        #print(self.blobs[sha])


    #извлечение информации о коммитах
    def parse_commit(self, commit_sha):
        #print(commit_sha)
        content = self.read_object(commit_sha)
        if type(content) == bytes:
            content = content.decode()
            lines = content.splitlines()

            tree_sha = lines[0].split()[1]  # первая строка имеет формат tree <sha>
            if lines[1].split()[0].startswith('parent'):
                # список родительских коммитов
                parent_shas = [line.split()[1] for line in lines[1:] if line.startswith('parent')]
                #print(parent_shas)
                for i in range(len(parent_shas)):
                    # print(self.commits[commit_sha]['parents'][i])
                    self.parse_commit(parent_shas[i])
            return
        #print(content,'\n')
        lines = content.splitlines()

        tree_sha = lines[0].split()[1] #первая строка имеет формат tree <sha>
        if lines[1].split()[0].startswith('parent'):
            # список родительских коммитов
            parent_shas = [line.split()[1] for line in lines[1:] if line.startswith('parent')]
            self.commits[commit_sha] = {
                'tree': tree_sha,
                'parents': parent_shas
            }
        else:
            self.commits[commit_sha] = {
                'tree': tree_sha,
                'parents': ''
            }

        #       print(self.commits)
        #print()

        if (self.commits[commit_sha]['parents'] != ''):
            for i in range(len(self.commits[commit_sha]['parents'])):
                #print(self.commits[commit_sha]['parents'][i])
                self.parse_commit(self.commits[commit_sha]['parents'][i])
        else:
            #print(0)
            return

    # извлечение информации о деревьях
    def parse_tree(self, tree_sha):
        #print(tree_sha)
        self.read_object_tree(tree_sha)#.decode(errors = 'replace')
        # print('\n',content)
        # entries = []
        # for line in content.splitlines():
        #     #Разделяет строку на части, извлекая режим доступа, имя файла и sha
        #     mode, filename, sha = line.split()[:3]
        #     entries.append((mode, filename, sha))
        # self.trees[tree_sha] = entries #Сохраняет информацию о дереве в словаре self.trees,
        # # где ключом является sha дерева, а значением — список записей о файлах и поддеревьях
        # return entries

    #генерация кода для визуализации
    def generate_plantuml(self):
        output = ["@startuml"]
        for commit_sha, commit in self.commits.items():
            #output.append(f'"commit {commit_sha[:7]}" : {commit["tree"][:7]}')
            #print(output)
            for parent in commit['parents']:
                output.append(f'"commit {parent[:7]}" --> "commit {commit_sha[:7]}"')
            output.append(f'{commit["tree"][:7]} : tree')
            output.append(f'"commit {commit_sha[:7]}" --> {commit["tree"][:7]}')
            # визуализация файловой системы
            # if commit['tree'] in self.trees:
            #     for mode, filename, sha in self.trees[commit['tree']]:
            #         output.append(f"file {filename} : {sha}")
        for tree in self.blobs:
            #print(tree)
            if not f'{tree["blob"][:7]} : blob' in output:
                output.append(f'{tree["blob"][:7]} : blob')
            if not f'"{tree["parent"][:7]}" -> {tree["blob"][:7]} : {tree["name"]}' in output:
                output.append(f'"{tree["parent"][:7]}" -> {tree["blob"][:7]} : {tree["name"]}')
        output.append("@enduml")
#для каждого хэша блоба в blobs список со словарями или переделать, чтоб был список словарей
        return "\n".join(output)

    def visualize(self):
        # Начнем с HEAD
        with open((self.repo_path+ '/.git'+ '/HEAD'), 'r') as f:
            ref = f.readline().strip()
            if ref.startswith('ref:'):
                branch_ref = ref.split(' ')[1]
                branch_path = (self.repo_path + '/.git/' +branch_ref)
                with open(branch_path, 'r') as br:
                    head_commit = br.readline().strip()
                    self.parse_commit(head_commit)
        for commit_sha, commit in self.commits.items():
            #print(commit["tree"])
            self.parse_tree(commit["tree"])


        plantuml_output = self.generate_plantuml()
        #print(plantuml_output)
        return str(plantuml_output)

    # def collect_commits(self, commit_sha):
    #     #print(commit_sha)
    #     if commit_sha not in self.commits:
    #         tree_sha = self.parse_commit(commit_sha)
    #         print(self.parse_tree(tree_sha))
    #         for parent in self.commits[commit_sha]['parents']:
    #             self.collect_commits(parent)

if __name__ == "__main__":

    #print(datetime.utcfromtimestamp(1729519378).strftime('%Y-%m-%d %H:%M:%S'))
    #print(zlib.decompress(b'01/55eb4229851634a0f03eb265b69f5a2d56f341'))

    #repo_path = "../.venv/project_1"
    visualizer = GitVisualizer(repo_path, date)
    f = open(result_file,'w')
    g = visualizer.visualize()
    f.write(g)
    print("Код записан в файл "+result_file+":\n")
    print(g)

