ENTRY(main)
SECTIONS {
  . = 0x10000;
  .text : { *(.text .text.*) }
  . = 0x20000;
  .rodata : { *(.rodata .rodata.*) }
  .data : { *(.sdata .sdata.*) *(.data .data.*) }
  .bss : { *(.sbss .sbss.*) *(.bss .bss.*) *(COMMON) }
}
