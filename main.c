#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Definição de uma struct
struct Pessoa {
    char nome[50];
    int idade;
};

// Função simples
int soma(int a, int b) {
    return a + b;
}

// Função com ponteiro para alterar o valor original
void dobrar(int *num) {
    *num *= 2;
}

int main() {
    // Declaração de variáveis básicas
    int inteiro = 10;
    float flutuante = 5.5;
    char caractere = 'A';
    char string[20] = "Olá, C!";

    // Impressão de variáveis
    printf("Inteiro: %d\n", inteiro);
    printf("Float: %.2f\n", flutuante);
    printf("Caractere: %c\n", caractere);
    printf("String: %s\n", string);

    // Entrada de dados
    printf("Digite um número inteiro: ");
    scanf("%d", &inteiro);
    printf("Você digitou: %d\n", inteiro);

    // Estruturas de controle
    if (inteiro > 10) {
        printf("O número é maior que 10.\n");
    } else if (inteiro == 10) {
        printf("O número é exatamente 10.\n");
    } else {
        printf("O número é menor que 10.\n");
    }

    // Loop for
    for (int i = 0; i < 5; i++) {
        printf("Loop for: %d\n", i);
    }

    // Loop while
    int contador = 0;
    while (contador < 3) {
        printf("Loop while: %d\n", contador);
        contador++;
    }

    // Switch-case
    switch (inteiro) {
        case 1:
            printf("Você digitou 1.\n");
            break;
        case 2:
            printf("Você digitou 2.\n");
            break;
        default:
            printf("Número não reconhecido.\n");
    }

    // Arrays
    int numeros[5] = {1, 2, 3, 4, 5};
    printf("Primeiro elemento do array: %d\n", numeros[0]);

    // Ponteiros
    int *ptr = &inteiro;
    printf("Endereço de inteiro: %p, Valor: %d\n", ptr, *ptr);

    // Chamando função
    printf("Soma de 5 e 3: %d\n", soma(5, 3));

    // Usando função que modifica valor por ponteiro
    dobrar(&inteiro);
    printf("Valor dobrado: %d\n", inteiro);

    // Uso de struct
    struct Pessoa pessoa1;
    strcpy(pessoa1.nome, "Carlos");
    pessoa1.idade = 25;
    printf("Pessoa: %s, %d anos\n", pessoa1.nome, pessoa1.idade);

    // Alocação dinâmica de memória
    int *arrayDinamico = (int *)malloc(5 * sizeof(int));
    if (arrayDinamico == NULL) {
        printf("Erro ao alocar memória.\n");
        return 1;
    }
    for (int i = 0; i < 5; i++) {
        arrayDinamico[i] = i * 10;
        printf("Array Dinâmico[%d]: %d\n", i, arrayDinamico[i]);
    }
    free(arrayDinamico);

    return 0;
}
