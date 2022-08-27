import os
from datetime import datetime
from enum import Enum, unique

ASSEMBLER_PATH = '/Users/bekyiu/dev/guaProject/zoye/8/b/assembler'
VM_PATH = '/Users/bekyiu/dev/guaProject/zoye/8/b/vm'

EXCEPT_LINES = [
    'con instructionBinCode = enums.InstructionBinCode',
    'con registerBinCode = enums.RegisterBinCode',
    'con InstructionBinCode = enums.InstructionBinCode',
    'con InstructionType = enums.InstructionType',
    'con GuaEventType = gua_enums.GuaEventType',
    'con GuaMouseButton = gua_enums.GuaMouseButton',
    'con GuaKeycode = gua_enums.GuaKeycode',

    'con Set = ins.Set',
    'con Load = ins.Load',
    'con Add = ins.Add',
    'con Jump = ins.Jump',
    'con Halt = ins.Halt',
    'con Save = ins.Save',
    'con JumpIfLess = ins.JumpIfLess',
    'con Compare = ins.Compare',
    'con SaveFromRegister = ins.SaveFromRegister',

    'con Set2 = ins.Set2',
    'con Load2 = ins.Load2',
    'con Add2 = ins.Add2',
    'con Save2 = ins.Save2',
    'con Subtract2 = ins.Subtract2',
    'con LoadFromRegister = ins.LoadFromRegister',
    'con LoadFromRegister2 = ins.LoadFromRegister2',
    'con SaveFromRegister2 = ins.SaveFromRegister2',
    'con JumpFromRegister = ins.JumpFromRegister',

    'con JumpRelative = ins.JumpRelative',
    'con JumpRelativeIfLess = ins.JumpRelativeIfLess',
    'con ShiftRight = ins.ShiftRight',
    'con And = ins.And',
    'con Debug = ins.Debug',
]

# 有顺序需求
ASSEMBLER_FILENAME_ORDERS = {
    # 无依赖
    "util.gua": 0,
    "enums.gua": 10,

    "fonts.gua": 15,
    #
    "instruction.gua": 20,
    "pseudo_instruction.gua": 25,
    # instruction 及其子类全是 30

    # 这两个放最后
    "instruction_builder.gua": 40,
    "axe_assembler.gua": 50,

}
VM_FILENAME_ORDERS = {
    "util.gua": 0,
    "enums.gua": 10,

    "fonts.gua": 15,
    "guacanvas_enums.gua": 20,

    # 其他都是30

    "instruction_builder.gua": 90,
    "xvm.gua": 100,
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
            if 'con' in line and '=' in line and 'import' in line and ('pimport' not in line):
                continue
            if line.strip() in EXCEPT_LINES:
                continue
            if line[-1] != '\n':
                line += '\n'
            if 'util.' in line:
                print(f'去掉 util. "{line.strip()}"')
                line = line.replace('util.', '')
            if 'fonts.' in line:
                log(f'去掉 fonts. "{line.strip()}"', Color.BLUE)
                line = line.replace('fonts.', '')
            if line.strip() == 'con RegisterBinCode = {' \
                    or ('assembler' in source_path and line.strip() == 'con InstructionBinCode = {'):
                var = line.split(' ')[1]
                new_var = first_lower(var)
                log(f'转换 {var} -> {new_var}', Color.CYAN)
                line = line.replace(var, new_var)

            target.write(line)

    write_wrapper(target, source_path)


def write_wrapper(target, source_path):
    asm = """
// 包一层给测试
con machineCode = function(asm) {
    log('wrapper')
    var assembler = AxeAssembler.new()
    assembler.load(asm)
    return assembler.compile()
}
    """

    vm = """
// 包一层给测试
con XVM = class() {
    con new = function(bytes) {
        var this.xvm = AxeVM.new(bytes)
        var this.memory = this.xvm.memory.memory

        var this.register = {
            'pa': 0,
            'a1': 0,
            'a2': 0,
            'a3': 0,
            'c1': 0,
            'f1': 0,
        }
    }

    con syncRegs = function() {
        this.register = {
            'pa': this.xvm.pa.value,
            'a1': this.xvm.a1.value,
            'a2': this.xvm.a2.value,
            'a3': this.xvm.a3.value,
            'c1': this.xvm.c1.value,
            'f1': this.xvm.f1.value,
        }  
    }

    con run = function() {
        this.xvm.run()
        this.syncRegs()
    }
    
    con display = function() {
        this.xvm.display()
        this.syncRegs()
    }

    con runWithDisplay = function() {
        this.xvm.runWithDisplay()
        this.syncRegs()
    }
}
    """
    if 'vm' in source_path:
        target.write(vm)
    else:
        target.write(asm)


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
    merge(ASSEMBLER_PATH, '/Users/bekyiu/dev/pythonProject/hello/x16asm.gua')
    merge(VM_PATH, '/Users/bekyiu/dev/pythonProject/hello/x16vm.gua')
