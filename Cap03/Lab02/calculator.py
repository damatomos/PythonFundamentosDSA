# Calculadora em python

class Calculator:
    def sum(self, a, b):
        return a + b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        if b == 0: return -1
        return a / b

    def sub(self, a, b):
        return a - b

    def calc(self, opt, a, b):
        if opt == 1:
            return '%r + %r = %r' %(a, b, self.sum(a, b))
        elif opt == 2:
            return '%r - %r = %r' %(a, b, self.sub(a, b))
        elif opt == 3:
            return '%r * %r = %r' %(a, b, self.mul(a, b))
        elif opt == 4:
            return '%r / %r = %r' %(a, b, self.div(a, b))

calculator = Calculator()

while True:
    print('%sPython Calculator %s' % ('• ' * 8, '• ' * 8))
    print('\nSelecione o numero da operacao desejada:\n')
    print('1 - Soma')
    print('2 - Subtracao')
    print('3 - Multiplicacao')
    print('4 - Divisao\n')
    opt = int(input('Digite sua opcao (1/2/3/4): '))
    if not opt in [1, 2, 3, 4]: break
    a = float(input('Digite o primeiro numero: '))
    b = float(input('Digite o segundo numero: '))
    print(calculator.calc(opt, a, b))