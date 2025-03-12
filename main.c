#include <stdio.h>
#include <string.h>

struct Pessoa {
    char nome[50];
    int idade;
};

int soma(int a, int b) {
    return a + b;
}

void dobrarValor(int *num) {
    num= 2;
}

int main() {
    int num1, num2, resultado;
    char opcao;

    printf("Digite um número: ");
    scanf("%d", &num1);

    printf("Digite outro número: ");
    scanf("%d", &num2);

    if (num1 > num2) {
        printf("%d é maior que %d\n", num1, num2);
    } else if (num1 < num2) {
        printf("%d é menor que %d\n", num1, num2);
    } else {
        printf("Os números são iguais!\n");
    }

    resultado = soma(num1, num2);
    printf("A soma é: %d\n", resultado);

    printf("Contagem: ");
    for (int i = 1; i <= 5; i++) {
        printf("%d ", i);
    }
    printf("\n");

    printf("Escolha uma opção (a/b/c): ");
    scanf(" %c", &opcao);

    switch (opcao) {
        case 'a': printf("Você escolheu A\n"); break;
        case 'b': printf("Você escolheu B\n"); break;
        case 'c': printf("Você escolheu C\n"); break;
        default: printf("Opção inválida!\n");
    }

    int valor = 10;
    printf("Valor antes: %d\n", valor);
    dobrarValor(&valor);
    printf("Valor depois: %d\n", valor);

    int numeros[3] = {1, 2, 3};
    printf("Elementos do array: ");
    for (int i = 0; i < 3; i++) {
        printf("%d ", numeros[i]);
    }
    printf("\n");
    //teste de comment
    struct Pessoa pessoa;
    strcpy(pessoa.nome, "Carlos");
    pessoa.idade = 25;
    printf("Nome: %s, Idade: %d\n", pessoa.nome, pessoa.idade);

    return 0;
}
