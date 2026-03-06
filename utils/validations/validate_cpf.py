def validate_cpf(cpf):
    # Cpf must have 11 digits
    if len(cpf) != 11:
        return False

    # Means that all the digits are equal
    if cpf == cpf[0] * 11:
        return False

    # valid the last 2 digits (JK) 10º and 11º
    sum2 = (int(cpf[0]) * 10 + int(cpf[1]) * 9 + int(cpf[2]) * 8 + int(cpf[3]) * 7 + int(cpf[4]) * 6 + int(cpf[5]) * 5 +
         int(cpf[6]) * 4 + int(cpf[7]) * 3 + int(cpf[8]) * 2)
    
    remainder = sum2 % 11
    
    if remainder < 2:
        j = 0
    else:
        j = 11 - remainder
    
    if str(j) != cpf[9]:
        return False

    sum3 = (int(cpf[0]) * 11 + int(cpf[1]) * 10 + int(cpf[2]) * 9 + int(cpf[3]) * 8 + int(cpf[4]) * 7 + int(cpf[5]) * 6 +
         int(cpf[6]) * 5 + int(cpf[7]) * 4 + int(cpf[8]) * 3 + int(cpf[9]) * 2)
    
    remainder2 = sum3  % 11

    if remainder2 < 2:
        k = 0
    else:
        k = 11 - remainder2
    
    if str(k) != cpf[10]:
        return False

    return True
