"""
Useful functions to interpret RV32I instructions
"""

def decode_rv32i_hex(hex_instruction: str):
    """
    Prints human readable assembly of hex RV32I instructions
    """
    # get 32-bit binary representation of a hex number
    instruction = bin(int(hex_instruction, 16))[2:].zfill(32)

    # decode bit fields
    shamt  = instruction[32 - 24 - 1:32 - 20]
    imm12  = instruction[32 - 31 - 1:32 - 20]
    rd     = instruction[32 - 11 - 1:32 - 7]
    funct3 = instruction[32 - 14 - 1:32 - 12]
    opcode = instruction[32 -  6 - 1:32 - 0]
    imm7   = instruction[32 - 31 - 1:32 - 25]
    funct7 = instruction[32 - 31 - 1:32 - 25]
    imm5   = instruction[32 - 11 - 1:32 - 7]
    rs1    = instruction[32 - 19 - 1:32 - 15]
    rs2    = instruction[32 - 24 - 1:32 - 20]

    # Decode I Instructions
    FORMAT_I = True
    ANDI = FORMAT_I and (funct3 == '111') and (opcode == '0010011')
    SLTIU = FORMAT_I and (funct3 == '011') and (opcode == '0010011')
    SRLI = FORMAT_I and (funct3 == '101') and (opcode == '0010011') and (funct7 == '0000000')
    SLTI = FORMAT_I and (funct3 == '010') and (opcode == '0010011')
    SRAI = FORMAT_I and (funct3 == '101') and (opcode == '0010011') and (funct7 == '0100000')
    SLLI = FORMAT_I and (funct3 == '001') and (opcode == '0010011') and (funct7 == '0000000')
    ORI = FORMAT_I and (funct3 == '110') and (opcode == '0010011')
    XORI = FORMAT_I and (funct3 == '100') and (opcode == '0010011')
    ADDI = FORMAT_I and (funct3 == '000') and (opcode == '0010011')
    ALLOWED_I = ANDI or SLTIU or SRLI or SLTI or SRAI or SLLI or ORI or XORI or ADDI

    # Decode LW Instructions
    FORMAT_LW = True #(instruction[32 - 31 - 1:32 - 30] == '00')
    LW = FORMAT_LW and (funct3 == '010') and (opcode == '0000011') and (rs1 == '00000')
    ALLOWED_LW = LW

    # Decode R Instructions
    FORMAT_R = True
    AND = FORMAT_R and (funct3 == '111') and (opcode == '0110011') and (funct7 == '0000000')
    SLTU = FORMAT_R and (funct3 == '011') and (opcode == '0110011') and (funct7 == '0000000')
    MULH = FORMAT_R and (funct3 == '001') and (opcode == '0110011') and (funct7 == '0000001')
    SRA = FORMAT_R and (funct3 == '101') and (opcode == '0110011') and (funct7 == '0100000')
    XOR = FORMAT_R and (funct3 == '100') and (opcode == '0110011') and (funct7 == '0000000')
    SUB = FORMAT_R and (funct3 == '000') and (opcode == '0110011') and (funct7 == '0100000')
    SLT = FORMAT_R and (funct3 == '010') and (opcode == '0110011') and (funct7 == '0000000')
    MULHSU = FORMAT_R and (funct3 == '010') and (opcode == '0110011') and (funct7 == '0000001')
    MULHU = FORMAT_R and (funct3 == '011') and (opcode == '0110011') and (funct7 == '0000001')
    SRL = FORMAT_R and (funct3 == '101') and (opcode == '0110011') and (funct7 == '0000000')
    SLL = FORMAT_R and (funct3 == '001') and (opcode == '0110011') and (funct7 == '0000000')
    ADD = FORMAT_R and (funct3 == '000') and (opcode == '0110011') and (funct7 == '0000000')
    MUL = FORMAT_R and (funct3 == '000') and (opcode == '0110011') and (funct7 == '0000001')
    OR = FORMAT_R and (funct3 == '110') and (opcode == '0110011') and (funct7 == '0000000')
    ALLOWED_R = AND or SLTU or MULH or SRA or XOR or SUB or SLT or MULHSU or\
        MULHU or SRL or SLL or ADD or MUL or OR

    # Decode SW Instructions
    FORMAT_SW = (instruction[32 - 31 - 1:32 - 30] == '00')
    SW = FORMAT_SW and (funct3 == '010') and (opcode == '0100011') and (rs1 == '00000')
    ALLOWED_SW = SW

    # Decode NOP
    NOP = (opcode == '1111111')
    ALLOWED_NOP = NOP

    # Find Assembly Opcode
    ASSEMBLY_OPS = ["ANDI", "SLTIU", "SRLI", "SLTI", "SRAI", "SLLI", "ORI", "XORI",
                    "ADDI", "LW", "AND", "SLTU", "MULH", "SRA", "XOR", "SUB",
                    "SLT", "MULHSU", "MULHU", "SRL", "SLL", "ADD", "MUL", "OR",
                    "SW"]
    decoded_ops = [ANDI, SLTIU, SRLI, SLTI, SRAI, SLLI, ORI, XORI,
                   ADDI, LW, AND, SLTU, MULH, SRA, XOR, SUB,
                   SLT, MULHSU, MULHU, SRL, SLL, ADD, MUL, OR,
                   SW]
    asm_op = None
    for i in range(len(decoded_ops)):
        if decoded_ops[i]:
            asm_op = ASSEMBLY_OPS[i]
            break
    assert asm_op is not None, "Error - Invalid Instruction"

    if ALLOWED_I:
        if SLLI or SRLI or SRAI:
            print('%s dst: %d src: %d shamt: %d' % (asm_op, int(rd, 2), int(rs1, 2), int(shamt, 2)))
        else:
            print('%s dst: %d src: %d imm: %d' % (asm_op, int(rd, 2), int(rs1, 2), int(imm12, 2)))

    elif ALLOWED_R:
        print('%s dst: %d src1: %d src2: %d' % (asm_op, int(rd, 2), int(rs1, 2), int(rs2, 2)))

    elif ALLOWED_LW:
        print('%s dst: %d base: %d offset: %d' % (asm_op, int(rd, 2), int(rs1, 2), int(imm12, 2)))

    elif ALLOWED_SW:
        print('%s src: %d base: %d offset: %d' % (asm_op, int(rs2, 2), int(rs1, 2), int(imm7 + imm5, 2)))

    elif ALLOWED_NOP:
        print(asm_op)
    else:
        print("Error - Invalid Instruction")


hex_inst_list = ['2802603', '6402423', '6802e03', '40005413', '5413']
for hex_inst in hex_inst_list:
    decode_rv32i_hex(hex_inst)
