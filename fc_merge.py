import os
from datetime import datetime
from enum import Enum, unique

ASSEMBLER_PATH = '/Users/bekyiu/dev/guaProject/zoye/fc/fc3/assembler'
VM_PATH = '/Users/bekyiu/dev/guaProject/zoye/fc/fc3/vm'

EXCEPT_LINES = [
    'con pseudoInstructionBuilder = ins.pseudoInstructionBuilder',
    'con instructionBuilder = ins.instructionBuilder',
    'con instructionBinCode = enums.instructionBinCode',

    'con memReg = enums.memReg',
    'con GuaEventType = gua_enums.GuaEventType',
    'con GuaMouseButton = gua_enums.GuaMouseButton',
    'con GuaKeycode = gua_enums.GuaKeycode',
    'con Keyboard = enums.Keyboard',

]

# 有顺序需求
ASSEMBLER_FILENAME_ORDERS = {
    # 无依赖
    "util.gua": 0,
    "enums.gua": 10,

    "instruction.gua": 20,

    "assembler.gua": 50,

}
VM_FILENAME_ORDERS = {
    "util.gua": 0,
    "enums.gua": 10,

    "guacanvas_enums.gua": 20,

    # 其他都是30

    "vm.gua": 100,
}


def sort_rule(orders, name, default=30):
    if name not in orders:
        return default
    return orders[name]


def list_files(path):
    dirs = os.listdir(path)
    orders = []
    if 'assembler' in path:
        print('\n========== assembler list ==========\n')
        orders = ASSEMBLER_FILENAME_ORDERS
    else:
        print('\n========== vm list ==========\n')
        orders = VM_FILENAME_ORDERS

    return sorted(dirs, key=lambda name: sort_rule(orders, name))


def first_lower(s):
    return s[:1].lower() + s[1:]


def merge(source_path, target_file):
    target = open(target_file, 'w', encoding='UTF-8')
    target.write(f'// ********** {datetime.now()} ***********\n')
    target.write('// 该文件由python生成, 仅用于提交作业; 实际开发在另一个分支\n')
    target.write('// *************************************************\n\n')
    for filename in list_files(source_path):
        file = source_path + os.sep + filename
        f = open(file, 'r', encoding='UTF-8')
        lines = f.readlines()
        for line in lines:
            if line.strip() in EXCEPT_LINES:
                continue
            if 'con' in line and '=' in line and 'import' in line and ('pimport' not in line):
                continue
            if line[-1] != '\n':
                line += '\n'
            if 'util.' in line:
                print(f'去掉 util. "{line.strip()}"')
                line = line.replace('util.', '')
            target.write(line)


@unique
class Color(Enum):
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37


def log(text, color):
    text = f'\033[0;{color.value}m{text}\033[0m'
    print(text)


if __name__ == '__main__':
    # merge(ASSEMBLER_PATH, '/Users/bekyiu/dev/pythonProject/hello/fc_asm.gua')
    # merge(VM_PATH, '/Users/bekyiu/dev/pythonProject/hello/fc_vm.gua')
    i = 3
    while i <= 8:
        merge(f'/Users/bekyiu/dev/guaProject/zoye/fc/fc{i}/assembler',
              f'/Users/bekyiu/dev/guaProject/zoye/fc/fc{i}/fc{i}.gua')

        merge(f'/Users/bekyiu/dev/guaProject/zoye/fc/fc{i}/vm',
              f'/Users/bekyiu/dev/guaProject/zoye/fc/fc{i}/nes{i}.gua')
        i += 1
