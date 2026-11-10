	.text
	.attribute	4, 16
	.attribute	5, "rv32i2p1_m2p0"
	.file	"main.c"
	.file	1 "C:/Users/HP/Desktop/genel codex i\303\247in/cmpe3209-proje" "main.c"
	.globl	mark_below                      # -- Begin function mark_below
	.p2align	2
	.type	mark_below,@function
mark_below:                             # @mark_below
.Lfunc_begin0:
	.cfi_sections .debug_frame
	.cfi_startproc
# %bb.0:
	#DEBUG_VALUE: mark_below:value <- $x10
	#DEBUG_VALUE: mark_below:average <- $x11
	.loc	1 9 15 prologue_end             # main.c:9:15
	slt	a1, a0, a1
.Ltmp0:
	.loc	1 9 9 is_stmt 0                 # main.c:9:9
	slli	a1, a1, 8
	or	a0, a0, a1
.Ltmp1:
	#DEBUG_VALUE: mark_below:value <- $x10
	.loc	1 11 5 is_stmt 1                # main.c:11:5
	ret
.Ltmp2:
.Lfunc_end0:
	.size	mark_below, .Lfunc_end0-mark_below
	.cfi_endproc
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	2
	.type	main,@function
main:                                   # @main
.Lfunc_begin1:
	.loc	1 15 0                          # main.c:15:0
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	s0, 12(sp)                      # 4-byte Folded Spill
	sw	s1, 8(sp)                       # 4-byte Folded Spill
	sw	s2, 4(sp)                       # 4-byte Folded Spill
	.cfi_offset s0, -4
	.cfi_offset s1, -8
	.cfi_offset s2, -12
	lui	a0, %hi(grades)
	addi	a0, a0, %lo(grades)
	lui	a1, 300
	addi	a1, a1, 1206
.Ltmp3:
	#DEBUG_VALUE: main:i <- 0
	#DEBUG_VALUE: main:pass <- 56
	#DEBUG_VALUE: main:sum <- 0
	#DEBUG_VALUE: main:x <- 1230006
	lui	a2, 406
	addi	a2, a2, 1549
	lui	a3, 247535
	addi	a3, a3, 863
	lui	a4, 1
	addi	a4, a4, 1095
	li	a5, 101
	addi	a6, a0, 120
.Ltmp4:
.LBB1_1:                                # =>This Inner Loop Header: Depth=1
	#DEBUG_VALUE: main:sum <- 0
	#DEBUG_VALUE: main:pass <- 56
	#DEBUG_VALUE: main:x <- $x11
	#DEBUG_VALUE: main:i <- [DW_OP_LLVM_arg 0, DW_OP_LLVM_arg 0, DW_OP_minus, DW_OP_consts 4, DW_OP_div, DW_OP_stack_value] undef
	.loc	1 19 22 prologue_end            # main.c:19:22
	mul	a1, a1, a2
.Ltmp5:
	.loc	1 19 26 is_stmt 0               # main.c:19:26
	add	a1, a1, a3
.Ltmp6:
	#DEBUG_VALUE: main:x <- $x11
	.loc	1 20 30 is_stmt 1               # main.c:20:30
	srli	a7, a1, 16
	.loc	1 20 37 is_stmt 0               # main.c:20:37
	mul	t0, a7, a4
	srli	t0, t0, 19
	mul	t0, t0, a5
	sub	a7, a7, t0
	slli	a7, a7, 16
	srli	a7, a7, 16
	.loc	1 20 19                         # main.c:20:19
	sw	a7, 0(a0)
.Ltmp7:
	#DEBUG_VALUE: main:i <- [DW_OP_LLVM_arg 0, DW_OP_LLVM_arg 0, DW_OP_minus, DW_OP_consts 4, DW_OP_div, DW_OP_consts 1, DW_OP_plus, DW_OP_stack_value] undef
	.loc	1 18 19 is_stmt 1               # main.c:18:19
	addi	a0, a0, 4
.Ltmp8:
	.loc	1 18 5 is_stmt 0                # main.c:18:5
	bne	a0, a6, .LBB1_1
.Ltmp9:
# %bb.2:
	#DEBUG_VALUE: main:x <- $x11
	#DEBUG_VALUE: main:sum <- 0
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 0 5                           # main.c:0:5
	li	a0, 0
	lui	a1, %hi(bucket)
.Ltmp10:
	addi	a2, a1, %lo(bucket)
	lw	a3, 16(a2)
	lw	a4, 12(a2)
	lw	a5, 8(a2)
	lw	a6, 4(a2)
	lui	a7, %hi(pass_count)
	lw	t0, %lo(pass_count)(a7)
	lui	t1, %hi(grades)
	addi	t1, t1, %lo(grades)
	lw	t2, %lo(bucket)(a1)
.Ltmp11:
	#DEBUG_VALUE: main:i <- 0
	#DEBUG_VALUE: main:sum <- 0
	li	t3, 49
	addi	t4, t1, 120
	li	t5, 65
	li	t6, 56
	li	s0, 74
	li	s1, 84
	j	.LBB1_5
.Ltmp12:
.LBB1_3:                                #   in Loop: Header=BB1_5 Depth=1
	#DEBUG_VALUE: v <- $x18
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 25 30 is_stmt 1               # main.c:25:30
	addi	t2, t2, 1
	sw	t2, %lo(bucket)(a1)
.Ltmp13:
.LBB1_4:                                #   in Loop: Header=BB1_5 Depth=1
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 22 19                         # main.c:22:19
	addi	t1, t1, 4
.Ltmp14:
	.loc	1 0 0 is_stmt 0                 # main.c:0:0
	add	a0, s2, a0
.Ltmp15:
	#DEBUG_VALUE: main:i <- [DW_OP_LLVM_arg 0, DW_OP_LLVM_arg 0, DW_OP_minus, DW_OP_consts 4, DW_OP_div, DW_OP_consts 1, DW_OP_plus, DW_OP_stack_value] undef
	#DEBUG_VALUE: main:sum <- $x10
	.loc	1 22 5                          # main.c:22:5
	beq	t1, t4, .LBB1_14
.Ltmp16:
.LBB1_5:                                # =>This Inner Loop Header: Depth=1
	#DEBUG_VALUE: main:pass <- 56
	#DEBUG_VALUE: main:sum <- $x10
	#DEBUG_VALUE: main:i <- [DW_OP_LLVM_arg 0, DW_OP_LLVM_arg 0, DW_OP_minus, DW_OP_consts 4, DW_OP_div, DW_OP_stack_value] undef
	.loc	1 23 17 is_stmt 1               # main.c:23:17
	lw	s2, 0(t1)
.Ltmp17:
	#DEBUG_VALUE: v <- $x18
	#DEBUG_VALUE: main:sum <- undef
	.loc	1 25 13                         # main.c:25:13
	bge	t3, s2, .LBB1_3
.Ltmp18:
# %bb.6:                                #   in Loop: Header=BB1_5 Depth=1
	#DEBUG_VALUE: v <- $x18
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 26 18                         # main.c:26:18
	bgeu	s2, t5, .LBB1_8
.Ltmp19:
# %bb.7:                                #   in Loop: Header=BB1_5 Depth=1
	#DEBUG_VALUE: v <- $x18
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 26 35 is_stmt 0               # main.c:26:35
	addi	a6, a6, 1
	sw	a6, 4(a2)
.Ltmp20:
	.loc	1 30 13 is_stmt 1               # main.c:30:13
	bltu	s2, t6, .LBB1_4
	j	.LBB1_13
.Ltmp21:
.LBB1_8:                                #   in Loop: Header=BB1_5 Depth=1
	#DEBUG_VALUE: v <- $x18
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 27 18                         # main.c:27:18
	bltu	s0, s2, .LBB1_10
.Ltmp22:
# %bb.9:                                #   in Loop: Header=BB1_5 Depth=1
	#DEBUG_VALUE: v <- $x18
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 27 35 is_stmt 0               # main.c:27:35
	addi	a5, a5, 1
	sw	a5, 8(a2)
	j	.LBB1_13
.Ltmp23:
.LBB1_10:                               #   in Loop: Header=BB1_5 Depth=1
	#DEBUG_VALUE: v <- $x18
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 28 18 is_stmt 1               # main.c:28:18
	bltu	s1, s2, .LBB1_12
.Ltmp24:
# %bb.11:                               #   in Loop: Header=BB1_5 Depth=1
	#DEBUG_VALUE: v <- $x18
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 28 35 is_stmt 0               # main.c:28:35
	addi	a4, a4, 1
	sw	a4, 12(a2)
	j	.LBB1_13
.Ltmp25:
.LBB1_12:                               #   in Loop: Header=BB1_5 Depth=1
	#DEBUG_VALUE: v <- $x18
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 29 23 is_stmt 1               # main.c:29:23
	addi	a3, a3, 1
	sw	a3, 16(a2)
.Ltmp26:
.LBB1_13:                               #   in Loop: Header=BB1_5 Depth=1
	#DEBUG_VALUE: v <- $x18
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 30 34                         # main.c:30:34
	addi	t0, t0, 1
	sw	t0, %lo(pass_count)(a7)
	j	.LBB1_4
.Ltmp27:
.LBB1_14:
	#DEBUG_VALUE: main:sum <- $x10
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 0 34 is_stmt 0                # main.c:0:34
	lui	a1, 559241
	addi	a1, a1, -1911
	.loc	1 32 16 is_stmt 1               # main.c:32:16
	mulh	a1, a0, a1
	add	a0, a1, a0
.Ltmp28:
	srli	a1, a0, 31
	srai	a0, a0, 4
	add	a0, a0, a1
	.loc	1 32 10 is_stmt 0               # main.c:32:10
	lui	a1, %hi(mean)
	sw	a0, %lo(mean)(a1)
.Ltmp29:
	#DEBUG_VALUE: main:i <- 0
	.loc	1 0 10                          # main.c:0:10
	lui	a1, %hi(below_count)
	lw	a2, %lo(below_count)(a1)
	lui	a3, %hi(grades)
	addi	a3, a3, %lo(grades)
	addi	a4, a3, 120
	j	.LBB1_16
.Ltmp30:
.LBB1_15:                               #   in Loop: Header=BB1_16 Depth=1
	#DEBUG_VALUE: main:pass <- 56
	#DEBUG_VALUE: main:i <- [DW_OP_LLVM_arg 0, DW_OP_LLVM_arg 0, DW_OP_minus, DW_OP_consts 4, DW_OP_div, DW_OP_consts 1, DW_OP_plus, DW_OP_stack_value] undef
	.loc	1 33 19 is_stmt 1               # main.c:33:19
	addi	a3, a3, 4
.Ltmp31:
	.loc	1 33 5 is_stmt 0                # main.c:33:5
	beq	a3, a4, .LBB1_18
.Ltmp32:
.LBB1_16:                               # =>This Inner Loop Header: Depth=1
	#DEBUG_VALUE: main:pass <- 56
	#DEBUG_VALUE: main:i <- [DW_OP_LLVM_arg 0, DW_OP_LLVM_arg 0, DW_OP_minus, DW_OP_consts 4, DW_OP_div, DW_OP_stack_value] undef
	.loc	1 34 17 is_stmt 1               # main.c:34:17
	lw	a5, 0(a3)
.Ltmp33:
	#DEBUG_VALUE: mark_below:average <- $x10
	#DEBUG_VALUE: mark_below:value <- $x15
	#DEBUG_VALUE: v <- $x15
	.loc	1 9 15                          # main.c:9:15
	slt	a6, a5, a0
.Ltmp34:
	.loc	1 9 9 is_stmt 0                 # main.c:9:9
	slli	a6, a6, 8
	or	a5, a5, a6
.Ltmp35:
	#DEBUG_VALUE: mark_below:value <- $x15
	.loc	1 36 23 is_stmt 1               # main.c:36:23
	andi	a6, a5, 256
.Ltmp36:
	.loc	1 35 19                         # main.c:35:19
	sw	a5, 0(a3)
	.loc	1 36 13                         # main.c:36:13
	beqz	a6, .LBB1_15
.Ltmp37:
# %bb.17:                               #   in Loop: Header=BB1_16 Depth=1
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 36 43 is_stmt 0               # main.c:36:43
	addi	a2, a2, 1
	sw	a2, %lo(below_count)(a1)
	j	.LBB1_15
.Ltmp38:
.LBB1_18:
	#DEBUG_VALUE: main:pass <- 56
	.loc	1 38 5 is_stmt 1                # main.c:38:5
	li	a0, 0
	lw	s0, 12(sp)                      # 4-byte Folded Reload
	lw	s1, 8(sp)                       # 4-byte Folded Reload
	lw	s2, 4(sp)                       # 4-byte Folded Reload
	.loc	1 38 5 epilogue_begin is_stmt 0 # main.c:38:5
	addi	sp, sp, 16
	ret
.Ltmp39:
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.type	SID,@object                     # @SID
	.section	.rodata,"a",@progbits
	.globl	SID
	.p2align	2, 0x0
SID:
	.word	1230006                         # 0x12c4b6
	.size	SID, 4

	.type	grades,@object                  # @grades
	.bss
	.globl	grades
	.p2align	2, 0x0
grades:
	.zero	120
	.size	grades, 120

	.type	bucket,@object                  # @bucket
	.globl	bucket
	.p2align	2, 0x0
bucket:
	.zero	20
	.size	bucket, 20

	.type	pass_count,@object              # @pass_count
	.section	.sbss,"aw",@nobits
	.globl	pass_count
	.p2align	2, 0x0
pass_count:
	.word	0                               # 0x0
	.size	pass_count, 4

	.type	mean,@object                    # @mean
	.globl	mean
	.p2align	2, 0x0
mean:
	.word	0                               # 0x0
	.size	mean, 4

	.type	below_count,@object             # @below_count
	.globl	below_count
	.p2align	2, 0x0
below_count:
	.word	0                               # 0x0
	.size	below_count, 4

	.section	.debug_loc,"",@progbits
.Ldebug_loc0:
	.word	.Lfunc_begin0-.Lfunc_begin0
	.word	.Ltmp0-.Lfunc_begin0
	.half	1                               # Loc expr size
	.byte	91                              # DW_OP_reg11
	.word	0
	.word	0
.Ldebug_loc1:
	.word	.Ltmp3-.Lfunc_begin0
	.word	.Ltmp4-.Lfunc_begin0
	.half	3                               # Loc expr size
	.byte	17                              # DW_OP_consts
	.byte	0                               # 0
	.byte	159                             # DW_OP_stack_value
	.word	.Ltmp11-.Lfunc_begin0
	.word	.Ltmp12-.Lfunc_begin0
	.half	3                               # Loc expr size
	.byte	17                              # DW_OP_consts
	.byte	0                               # 0
	.byte	159                             # DW_OP_stack_value
	.word	.Ltmp29-.Lfunc_begin0
	.word	.Ltmp30-.Lfunc_begin0
	.half	3                               # Loc expr size
	.byte	17                              # DW_OP_consts
	.byte	0                               # 0
	.byte	159                             # DW_OP_stack_value
	.word	0
	.word	0
.Ldebug_loc2:
	.word	.Ltmp3-.Lfunc_begin0
	.word	.Ltmp12-.Lfunc_begin0
	.half	3                               # Loc expr size
	.byte	17                              # DW_OP_consts
	.byte	0                               # 0
	.byte	159                             # DW_OP_stack_value
	.word	.Ltmp15-.Lfunc_begin0
	.word	.Ltmp17-.Lfunc_begin0
	.half	1                               # Loc expr size
	.byte	90                              # DW_OP_reg10
	.word	.Ltmp27-.Lfunc_begin0
	.word	.Ltmp28-.Lfunc_begin0
	.half	1                               # Loc expr size
	.byte	90                              # DW_OP_reg10
	.word	0
	.word	0
.Ldebug_loc3:
	.word	.Ltmp3-.Lfunc_begin0
	.word	.Ltmp4-.Lfunc_begin0
	.half	5                               # Loc expr size
	.byte	16                              # DW_OP_constu
	.byte	182                             # 1230006
	.byte	137                             # 
	.byte	75                              # 
	.byte	159                             # DW_OP_stack_value
	.word	.Ltmp4-.Lfunc_begin0
	.word	.Ltmp5-.Lfunc_begin0
	.half	1                               # Loc expr size
	.byte	91                              # DW_OP_reg11
	.word	.Ltmp6-.Lfunc_begin0
	.word	.Ltmp10-.Lfunc_begin0
	.half	1                               # Loc expr size
	.byte	91                              # DW_OP_reg11
	.word	0
	.word	0
.Ldebug_loc4:
	.word	.Ltmp12-.Lfunc_begin0
	.word	.Ltmp13-.Lfunc_begin0
	.half	1                               # Loc expr size
	.byte	98                              # DW_OP_reg18
	.word	.Ltmp17-.Lfunc_begin0
	.word	.Ltmp27-.Lfunc_begin0
	.half	1                               # Loc expr size
	.byte	98                              # DW_OP_reg18
	.word	0
	.word	0
.Ldebug_loc5:
	.word	.Ltmp33-.Lfunc_begin0
	.word	.Ltmp35-.Lfunc_begin0
	.half	1                               # Loc expr size
	.byte	95                              # DW_OP_reg15
	.word	0
	.word	0
	.section	.debug_abbrev,"",@progbits
	.byte	1                               # Abbreviation Code
	.byte	17                              # DW_TAG_compile_unit
	.byte	1                               # DW_CHILDREN_yes
	.byte	37                              # DW_AT_producer
	.byte	14                              # DW_FORM_strp
	.byte	19                              # DW_AT_language
	.byte	5                               # DW_FORM_data2
	.byte	3                               # DW_AT_name
	.byte	14                              # DW_FORM_strp
	.byte	16                              # DW_AT_stmt_list
	.byte	23                              # DW_FORM_sec_offset
	.byte	27                              # DW_AT_comp_dir
	.byte	14                              # DW_FORM_strp
	.byte	17                              # DW_AT_low_pc
	.byte	1                               # DW_FORM_addr
	.byte	18                              # DW_AT_high_pc
	.byte	6                               # DW_FORM_data4
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	2                               # Abbreviation Code
	.byte	52                              # DW_TAG_variable
	.byte	0                               # DW_CHILDREN_no
	.byte	3                               # DW_AT_name
	.byte	14                              # DW_FORM_strp
	.byte	73                              # DW_AT_type
	.byte	19                              # DW_FORM_ref4
	.byte	63                              # DW_AT_external
	.byte	25                              # DW_FORM_flag_present
	.byte	58                              # DW_AT_decl_file
	.byte	11                              # DW_FORM_data1
	.byte	59                              # DW_AT_decl_line
	.byte	11                              # DW_FORM_data1
	.byte	2                               # DW_AT_location
	.byte	24                              # DW_FORM_exprloc
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	3                               # Abbreviation Code
	.byte	38                              # DW_TAG_const_type
	.byte	0                               # DW_CHILDREN_no
	.byte	73                              # DW_AT_type
	.byte	19                              # DW_FORM_ref4
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	4                               # Abbreviation Code
	.byte	36                              # DW_TAG_base_type
	.byte	0                               # DW_CHILDREN_no
	.byte	3                               # DW_AT_name
	.byte	14                              # DW_FORM_strp
	.byte	62                              # DW_AT_encoding
	.byte	11                              # DW_FORM_data1
	.byte	11                              # DW_AT_byte_size
	.byte	11                              # DW_FORM_data1
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	5                               # Abbreviation Code
	.byte	1                               # DW_TAG_array_type
	.byte	1                               # DW_CHILDREN_yes
	.byte	73                              # DW_AT_type
	.byte	19                              # DW_FORM_ref4
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	6                               # Abbreviation Code
	.byte	33                              # DW_TAG_subrange_type
	.byte	0                               # DW_CHILDREN_no
	.byte	73                              # DW_AT_type
	.byte	19                              # DW_FORM_ref4
	.byte	55                              # DW_AT_count
	.byte	11                              # DW_FORM_data1
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	7                               # Abbreviation Code
	.byte	36                              # DW_TAG_base_type
	.byte	0                               # DW_CHILDREN_no
	.byte	3                               # DW_AT_name
	.byte	14                              # DW_FORM_strp
	.byte	11                              # DW_AT_byte_size
	.byte	11                              # DW_FORM_data1
	.byte	62                              # DW_AT_encoding
	.byte	11                              # DW_FORM_data1
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	8                               # Abbreviation Code
	.byte	4                               # DW_TAG_enumeration_type
	.byte	1                               # DW_CHILDREN_yes
	.byte	73                              # DW_AT_type
	.byte	19                              # DW_FORM_ref4
	.byte	11                              # DW_AT_byte_size
	.byte	11                              # DW_FORM_data1
	.byte	58                              # DW_AT_decl_file
	.byte	11                              # DW_FORM_data1
	.byte	59                              # DW_AT_decl_line
	.byte	11                              # DW_FORM_data1
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	9                               # Abbreviation Code
	.byte	40                              # DW_TAG_enumerator
	.byte	0                               # DW_CHILDREN_no
	.byte	3                               # DW_AT_name
	.byte	14                              # DW_FORM_strp
	.byte	28                              # DW_AT_const_value
	.byte	15                              # DW_FORM_udata
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	10                              # Abbreviation Code
	.byte	46                              # DW_TAG_subprogram
	.byte	1                               # DW_CHILDREN_yes
	.byte	17                              # DW_AT_low_pc
	.byte	1                               # DW_FORM_addr
	.byte	18                              # DW_AT_high_pc
	.byte	6                               # DW_FORM_data4
	.byte	64                              # DW_AT_frame_base
	.byte	24                              # DW_FORM_exprloc
	.ascii	"\227B"                         # DW_AT_GNU_all_call_sites
	.byte	25                              # DW_FORM_flag_present
	.byte	49                              # DW_AT_abstract_origin
	.byte	19                              # DW_FORM_ref4
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	11                              # Abbreviation Code
	.byte	5                               # DW_TAG_formal_parameter
	.byte	0                               # DW_CHILDREN_no
	.byte	2                               # DW_AT_location
	.byte	24                              # DW_FORM_exprloc
	.byte	49                              # DW_AT_abstract_origin
	.byte	19                              # DW_FORM_ref4
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	12                              # Abbreviation Code
	.byte	5                               # DW_TAG_formal_parameter
	.byte	0                               # DW_CHILDREN_no
	.byte	2                               # DW_AT_location
	.byte	23                              # DW_FORM_sec_offset
	.byte	49                              # DW_AT_abstract_origin
	.byte	19                              # DW_FORM_ref4
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	13                              # Abbreviation Code
	.byte	46                              # DW_TAG_subprogram
	.byte	1                               # DW_CHILDREN_yes
	.byte	3                               # DW_AT_name
	.byte	14                              # DW_FORM_strp
	.byte	58                              # DW_AT_decl_file
	.byte	11                              # DW_FORM_data1
	.byte	59                              # DW_AT_decl_line
	.byte	11                              # DW_FORM_data1
	.byte	39                              # DW_AT_prototyped
	.byte	25                              # DW_FORM_flag_present
	.byte	73                              # DW_AT_type
	.byte	19                              # DW_FORM_ref4
	.byte	63                              # DW_AT_external
	.byte	25                              # DW_FORM_flag_present
	.byte	32                              # DW_AT_inline
	.byte	11                              # DW_FORM_data1
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	14                              # Abbreviation Code
	.byte	5                               # DW_TAG_formal_parameter
	.byte	0                               # DW_CHILDREN_no
	.byte	3                               # DW_AT_name
	.byte	14                              # DW_FORM_strp
	.byte	58                              # DW_AT_decl_file
	.byte	11                              # DW_FORM_data1
	.byte	59                              # DW_AT_decl_line
	.byte	11                              # DW_FORM_data1
	.byte	73                              # DW_AT_type
	.byte	19                              # DW_FORM_ref4
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	15                              # Abbreviation Code
	.byte	46                              # DW_TAG_subprogram
	.byte	1                               # DW_CHILDREN_yes
	.byte	17                              # DW_AT_low_pc
	.byte	1                               # DW_FORM_addr
	.byte	18                              # DW_AT_high_pc
	.byte	6                               # DW_FORM_data4
	.byte	64                              # DW_AT_frame_base
	.byte	24                              # DW_FORM_exprloc
	.ascii	"\227B"                         # DW_AT_GNU_all_call_sites
	.byte	25                              # DW_FORM_flag_present
	.byte	3                               # DW_AT_name
	.byte	14                              # DW_FORM_strp
	.byte	58                              # DW_AT_decl_file
	.byte	11                              # DW_FORM_data1
	.byte	59                              # DW_AT_decl_line
	.byte	11                              # DW_FORM_data1
	.byte	39                              # DW_AT_prototyped
	.byte	25                              # DW_FORM_flag_present
	.byte	73                              # DW_AT_type
	.byte	19                              # DW_FORM_ref4
	.byte	63                              # DW_AT_external
	.byte	25                              # DW_FORM_flag_present
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	16                              # Abbreviation Code
	.byte	52                              # DW_TAG_variable
	.byte	0                               # DW_CHILDREN_no
	.byte	2                               # DW_AT_location
	.byte	23                              # DW_FORM_sec_offset
	.byte	3                               # DW_AT_name
	.byte	14                              # DW_FORM_strp
	.byte	58                              # DW_AT_decl_file
	.byte	11                              # DW_FORM_data1
	.byte	59                              # DW_AT_decl_line
	.byte	11                              # DW_FORM_data1
	.byte	73                              # DW_AT_type
	.byte	19                              # DW_FORM_ref4
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	17                              # Abbreviation Code
	.byte	52                              # DW_TAG_variable
	.byte	0                               # DW_CHILDREN_no
	.byte	28                              # DW_AT_const_value
	.byte	13                              # DW_FORM_sdata
	.byte	3                               # DW_AT_name
	.byte	14                              # DW_FORM_strp
	.byte	58                              # DW_AT_decl_file
	.byte	11                              # DW_FORM_data1
	.byte	59                              # DW_AT_decl_line
	.byte	11                              # DW_FORM_data1
	.byte	73                              # DW_AT_type
	.byte	19                              # DW_FORM_ref4
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	18                              # Abbreviation Code
	.byte	11                              # DW_TAG_lexical_block
	.byte	1                               # DW_CHILDREN_yes
	.byte	85                              # DW_AT_ranges
	.byte	23                              # DW_FORM_sec_offset
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	19                              # Abbreviation Code
	.byte	11                              # DW_TAG_lexical_block
	.byte	1                               # DW_CHILDREN_yes
	.byte	17                              # DW_AT_low_pc
	.byte	1                               # DW_FORM_addr
	.byte	18                              # DW_AT_high_pc
	.byte	6                               # DW_FORM_data4
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	20                              # Abbreviation Code
	.byte	29                              # DW_TAG_inlined_subroutine
	.byte	1                               # DW_CHILDREN_yes
	.byte	49                              # DW_AT_abstract_origin
	.byte	19                              # DW_FORM_ref4
	.byte	17                              # DW_AT_low_pc
	.byte	1                               # DW_FORM_addr
	.byte	18                              # DW_AT_high_pc
	.byte	6                               # DW_FORM_data4
	.byte	88                              # DW_AT_call_file
	.byte	11                              # DW_FORM_data1
	.byte	89                              # DW_AT_call_line
	.byte	11                              # DW_FORM_data1
	.byte	87                              # DW_AT_call_column
	.byte	11                              # DW_FORM_data1
	.byte	0                               # EOM(1)
	.byte	0                               # EOM(2)
	.byte	0                               # EOM(3)
	.section	.debug_info,"",@progbits
.Lcu_begin0:
	.word	.Ldebug_info_end0-.Ldebug_info_start0 # Length of Unit
.Ldebug_info_start0:
	.half	4                               # DWARF version number
	.word	.debug_abbrev                   # Offset Into Abbrev. Section
	.byte	4                               # Address Size (in bytes)
	.byte	1                               # Abbrev [1] 0xb:0x1a2 DW_TAG_compile_unit
	.word	.Linfo_string0                  # DW_AT_producer
	.half	12                              # DW_AT_language
	.word	.Linfo_string1                  # DW_AT_name
	.word	.Lline_table_start0             # DW_AT_stmt_list
	.word	.Linfo_string2                  # DW_AT_comp_dir
	.word	.Lfunc_begin0                   # DW_AT_low_pc
	.word	.Lfunc_end1-.Lfunc_begin0       # DW_AT_high_pc
	.byte	2                               # Abbrev [2] 0x26:0x11 DW_TAG_variable
	.word	.Linfo_string3                  # DW_AT_name
	.word	55                              # DW_AT_type
                                        # DW_AT_external
	.byte	1                               # DW_AT_decl_file
	.byte	2                               # DW_AT_decl_line
	.byte	5                               # DW_AT_location
	.byte	3
	.word	SID
	.byte	3                               # Abbrev [3] 0x37:0x5 DW_TAG_const_type
	.word	60                              # DW_AT_type
	.byte	4                               # Abbrev [4] 0x3c:0x7 DW_TAG_base_type
	.word	.Linfo_string4                  # DW_AT_name
	.byte	5                               # DW_AT_encoding
	.byte	4                               # DW_AT_byte_size
	.byte	2                               # Abbrev [2] 0x43:0x11 DW_TAG_variable
	.word	.Linfo_string5                  # DW_AT_name
	.word	84                              # DW_AT_type
                                        # DW_AT_external
	.byte	1                               # DW_AT_decl_file
	.byte	4                               # DW_AT_decl_line
	.byte	5                               # DW_AT_location
	.byte	3
	.word	grades
	.byte	5                               # Abbrev [5] 0x54:0xc DW_TAG_array_type
	.word	60                              # DW_AT_type
	.byte	6                               # Abbrev [6] 0x59:0x6 DW_TAG_subrange_type
	.word	96                              # DW_AT_type
	.byte	30                              # DW_AT_count
	.byte	0                               # End Of Children Mark
	.byte	7                               # Abbrev [7] 0x60:0x7 DW_TAG_base_type
	.word	.Linfo_string6                  # DW_AT_name
	.byte	8                               # DW_AT_byte_size
	.byte	7                               # DW_AT_encoding
	.byte	2                               # Abbrev [2] 0x67:0x11 DW_TAG_variable
	.word	.Linfo_string7                  # DW_AT_name
	.word	120                             # DW_AT_type
                                        # DW_AT_external
	.byte	1                               # DW_AT_decl_file
	.byte	5                               # DW_AT_decl_line
	.byte	5                               # DW_AT_location
	.byte	3
	.word	bucket
	.byte	5                               # Abbrev [5] 0x78:0xc DW_TAG_array_type
	.word	60                              # DW_AT_type
	.byte	6                               # Abbrev [6] 0x7d:0x6 DW_TAG_subrange_type
	.word	96                              # DW_AT_type
	.byte	5                               # DW_AT_count
	.byte	0                               # End Of Children Mark
	.byte	2                               # Abbrev [2] 0x84:0x11 DW_TAG_variable
	.word	.Linfo_string8                  # DW_AT_name
	.word	60                              # DW_AT_type
                                        # DW_AT_external
	.byte	1                               # DW_AT_decl_file
	.byte	5                               # DW_AT_decl_line
	.byte	5                               # DW_AT_location
	.byte	3
	.word	mean
	.byte	2                               # Abbrev [2] 0x95:0x11 DW_TAG_variable
	.word	.Linfo_string9                  # DW_AT_name
	.word	60                              # DW_AT_type
                                        # DW_AT_external
	.byte	1                               # DW_AT_decl_file
	.byte	5                               # DW_AT_decl_line
	.byte	5                               # DW_AT_location
	.byte	3
	.word	below_count
	.byte	2                               # Abbrev [2] 0xa6:0x11 DW_TAG_variable
	.word	.Linfo_string10                 # DW_AT_name
	.word	60                              # DW_AT_type
                                        # DW_AT_external
	.byte	1                               # DW_AT_decl_file
	.byte	5                               # DW_AT_decl_line
	.byte	5                               # DW_AT_location
	.byte	3
	.word	pass_count
	.byte	8                               # Abbrev [8] 0xb7:0xf DW_TAG_enumeration_type
	.word	198                             # DW_AT_type
	.byte	4                               # DW_AT_byte_size
	.byte	1                               # DW_AT_decl_file
	.byte	3                               # DW_AT_decl_line
	.byte	9                               # Abbrev [9] 0xbf:0x6 DW_TAG_enumerator
	.word	.Linfo_string12                 # DW_AT_name
	.byte	30                              # DW_AT_const_value
	.byte	0                               # End Of Children Mark
	.byte	4                               # Abbrev [4] 0xc6:0x7 DW_TAG_base_type
	.word	.Linfo_string11                 # DW_AT_name
	.byte	7                               # DW_AT_encoding
	.byte	4                               # DW_AT_byte_size
	.byte	10                              # Abbrev [10] 0xcd:0x20 DW_TAG_subprogram
	.word	.Lfunc_begin0                   # DW_AT_low_pc
	.word	.Lfunc_end0-.Lfunc_begin0       # DW_AT_high_pc
	.byte	1                               # DW_AT_frame_base
	.byte	82
                                        # DW_AT_GNU_all_call_sites
	.word	237                             # DW_AT_abstract_origin
	.byte	11                              # Abbrev [11] 0xdc:0x7 DW_TAG_formal_parameter
	.byte	1                               # DW_AT_location
	.byte	90
	.word	249                             # DW_AT_abstract_origin
	.byte	12                              # Abbrev [12] 0xe3:0x9 DW_TAG_formal_parameter
	.word	.Ldebug_loc0                    # DW_AT_location
	.word	260                             # DW_AT_abstract_origin
	.byte	0                               # End Of Children Mark
	.byte	13                              # Abbrev [13] 0xed:0x23 DW_TAG_subprogram
	.word	.Linfo_string13                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	7                               # DW_AT_decl_line
                                        # DW_AT_prototyped
	.word	60                              # DW_AT_type
                                        # DW_AT_external
	.byte	1                               # DW_AT_inline
	.byte	14                              # Abbrev [14] 0xf9:0xb DW_TAG_formal_parameter
	.word	.Linfo_string14                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	7                               # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	14                              # Abbrev [14] 0x104:0xb DW_TAG_formal_parameter
	.word	.Linfo_string15                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	7                               # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	0                               # End Of Children Mark
	.byte	15                              # Abbrev [15] 0x110:0x9c DW_TAG_subprogram
	.word	.Lfunc_begin1                   # DW_AT_low_pc
	.word	.Lfunc_end1-.Lfunc_begin1       # DW_AT_high_pc
	.byte	1                               # DW_AT_frame_base
	.byte	82
                                        # DW_AT_GNU_all_call_sites
	.word	.Linfo_string16                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	14                              # DW_AT_decl_line
                                        # DW_AT_prototyped
	.word	60                              # DW_AT_type
                                        # DW_AT_external
	.byte	16                              # Abbrev [16] 0x125:0xf DW_TAG_variable
	.word	.Ldebug_loc1                    # DW_AT_location
	.word	.Linfo_string17                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	17                              # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	17                              # Abbrev [17] 0x134:0xc DW_TAG_variable
	.byte	56                              # DW_AT_const_value
	.word	.Linfo_string18                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	17                              # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	16                              # Abbrev [16] 0x140:0xf DW_TAG_variable
	.word	.Ldebug_loc2                    # DW_AT_location
	.word	.Linfo_string19                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	17                              # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	16                              # Abbrev [16] 0x14f:0xf DW_TAG_variable
	.word	.Ldebug_loc3                    # DW_AT_location
	.word	.Linfo_string20                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	16                              # DW_AT_decl_line
	.word	198                             # DW_AT_type
	.byte	18                              # Abbrev [18] 0x15e:0x15 DW_TAG_lexical_block
	.word	.Ldebug_ranges0                 # DW_AT_ranges
	.byte	16                              # Abbrev [16] 0x163:0xf DW_TAG_variable
	.word	.Ldebug_loc4                    # DW_AT_location
	.word	.Linfo_string21                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	23                              # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	0                               # End Of Children Mark
	.byte	19                              # Abbrev [19] 0x173:0x38 DW_TAG_lexical_block
	.word	.Ltmp32                         # DW_AT_low_pc
	.word	.Ltmp38-.Ltmp32                 # DW_AT_high_pc
	.byte	16                              # Abbrev [16] 0x17c:0xf DW_TAG_variable
	.word	.Ldebug_loc5                    # DW_AT_location
	.word	.Linfo_string21                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	34                              # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	20                              # Abbrev [20] 0x18b:0x1f DW_TAG_inlined_subroutine
	.word	237                             # DW_AT_abstract_origin
	.word	.Ltmp33                         # DW_AT_low_pc
	.word	.Ltmp35-.Ltmp33                 # DW_AT_high_pc
	.byte	1                               # DW_AT_call_file
	.byte	35                              # DW_AT_call_line
	.byte	21                              # DW_AT_call_column
	.byte	11                              # Abbrev [11] 0x19b:0x7 DW_TAG_formal_parameter
	.byte	1                               # DW_AT_location
	.byte	95
	.word	249                             # DW_AT_abstract_origin
	.byte	11                              # Abbrev [11] 0x1a2:0x7 DW_TAG_formal_parameter
	.byte	1                               # DW_AT_location
	.byte	90
	.word	260                             # DW_AT_abstract_origin
	.byte	0                               # End Of Children Mark
	.byte	0                               # End Of Children Mark
	.byte	0                               # End Of Children Mark
	.byte	0                               # End Of Children Mark
.Ldebug_info_end0:
	.section	.debug_ranges,"",@progbits
.Ldebug_ranges0:
	.word	.Ltmp12-.Lfunc_begin0
	.word	.Ltmp13-.Lfunc_begin0
	.word	.Ltmp16-.Lfunc_begin0
	.word	.Ltmp27-.Lfunc_begin0
	.word	0
	.word	0
	.section	.debug_str,"MS",@progbits,1
.Linfo_string0:
	.asciz	"clang version 18.1.6 (https://github.com/ziglang/zig-bootstrap 98bc6bf4fc4009888d33941daf6b600d20a42a56)" # string offset=0
.Linfo_string1:
	.asciz	"main.c"                        # string offset=105
.Linfo_string2:
	.asciz	"C:/Users/HP/Desktop/genel codex i\303\247in/cmpe3209-proje" # string offset=112
.Linfo_string3:
	.asciz	"SID"                           # string offset=165
.Linfo_string4:
	.asciz	"int"                           # string offset=169
.Linfo_string5:
	.asciz	"grades"                        # string offset=173
.Linfo_string6:
	.asciz	"__ARRAY_SIZE_TYPE__"           # string offset=180
.Linfo_string7:
	.asciz	"bucket"                        # string offset=200
.Linfo_string8:
	.asciz	"mean"                          # string offset=207
.Linfo_string9:
	.asciz	"below_count"                   # string offset=212
.Linfo_string10:
	.asciz	"pass_count"                    # string offset=224
.Linfo_string11:
	.asciz	"unsigned int"                  # string offset=235
.Linfo_string12:
	.asciz	"N"                             # string offset=248
.Linfo_string13:
	.asciz	"mark_below"                    # string offset=250
.Linfo_string14:
	.asciz	"value"                         # string offset=261
.Linfo_string15:
	.asciz	"average"                       # string offset=267
.Linfo_string16:
	.asciz	"main"                          # string offset=275
.Linfo_string17:
	.asciz	"i"                             # string offset=280
.Linfo_string18:
	.asciz	"pass"                          # string offset=282
.Linfo_string19:
	.asciz	"sum"                           # string offset=287
.Linfo_string20:
	.asciz	"x"                             # string offset=291
.Linfo_string21:
	.asciz	"v"                             # string offset=293
	.ident	"clang version 18.1.6 (https://github.com/ziglang/zig-bootstrap 98bc6bf4fc4009888d33941daf6b600d20a42a56)"
	.section	".note.GNU-stack","",@progbits
	.addrsig
	.section	.debug_line,"",@progbits
.Lline_table_start0:
