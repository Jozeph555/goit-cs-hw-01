.global _main
.extern _printf
.align 2

.text
_main:
    // Зберігаємо регістри
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    sub     sp, sp, #16         // Виділяємо місце в стеку

    // Виконуємо обчислення
    mov     w19, #3             // b = 3
    mov     w20, #2             // c = 2
    sub     w19, w19, w20       // b - c (3 - 2 = 1)
    mov     w20, #5             // a = 5
    add     w19, w19, w20       // (b - c) + a (1 + 5 = 6)

    // Зберігаємо результат
    str     w19, [sp]

    // Виводимо результат
    adrp    x0, formatStr@PAGE
    add     x0, x0, formatStr@PAGEOFF
    ldr     w1, [sp]            // Завантажуємо результат зі стеку
    bl      _printf

    // Відновлюємо стек і регістри
    add     sp, sp, #16
    ldp     x29, x30, [sp], #16
    
    // Повертаємо 0
    mov     w0, #0
    ret

.section __DATA,__data
formatStr:
    .asciz "Result: %d\n"
