.global _main
.align 2

.text
_main:
    // Зберігаємо регістри
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp

    // Завантажуємо та виконуємо обчислення
    adrp    x8, b@PAGE          // Завантажуємо адресу b
    add     x8, x8, b@PAGEOFF
    ldrb    w9, [x8]            // w9 = 3 (значення b)
    
    adrp    x8, c@PAGE          // Завантажуємо адресу c
    add     x8, x8, c@PAGEOFF
    ldrb    w10, [x8]           // w10 = 2 (значення c)
    sub     w9, w9, w10         // w9 = w9 - w10 (3 - 2)
    
    adrp    x8, a@PAGE          // Завантажуємо адресу a
    add     x8, x8, a@PAGEOFF
    ldrb    w10, [x8]           // w10 = 5 (значення a)
    add     w9, w9, w10         // w9 = w9 + w10 (1 + 5 = 6)

    // Конвертуємо число в ASCII (додаємо 48)
    add     w9, w9, #48         // Конвертуємо в ASCII символ

    // Виводимо "Result: "
    mov     x0, #1              // файловий дескриптор (1 = stdout)
    adrp    x1, resultMsg@PAGE  // адреса повідомлення
    add     x1, x1, resultMsg@PAGEOFF
    mov     x2, #8              // довжина повідомлення
    mov     x16, #4             // системний виклик write
    svc     #0x80               // викликаємо систему

    // Виводимо число
    sub     sp, sp, #16         // виділяємо місце в стеку для символу
    strb    w9, [sp, #8]        // зберігаємо символ
    mov     x0, #1              // stdout
    add     x1, sp, #8          // адреса символу
    mov     x2, #1              // довжина (1 символ)
    mov     x16, #4             // системний виклик write
    svc     #0x80               // викликаємо систему

    // Виводимо новий рядок
    adrp    x1, newline@PAGE
    add     x1, x1, newline@PAGEOFF
    mov     x0, #1
    mov     x2, #1
    mov     x16, #4
    svc     #0x80

    // Відновлюємо стек
    add     sp, sp, #16          // Відновлюємо стек

    // Відновлюємо регістри та повертаємося
    ldp     x29, x30, [sp], #16
    mov     x0, #0
    ret

.section __DATA,__data
a:
    .byte   5                   // a = 5
b:
    .byte   3                   // b = 3
c:
    .byte   2                   // c = 2
resultMsg:
    .ascii  "Result: "          // Без нульового байта
newline:
    .ascii  "\n"                // Символ нового рядка