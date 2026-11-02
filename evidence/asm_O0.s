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
	.loc	1 8 0                           # main.c:8:0
	.cfi_sections .debug_frame
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	ra, 12(sp)                      # 4-byte Folded Spill
	sw	s0, 8(sp)                       # 4-byte Folded Spill
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	addi	s0, sp, 16
	.cfi_def_cfa s0, 0
	sw	a0, -12(s0)
	sw	a1, -16(s0)
.Ltmp0:
	.loc	1 9 9 prologue_end              # main.c:9:9
	lw	a0, -12(s0)
	.loc	1 9 17 is_stmt 0                # main.c:9:17
	lw	a1, -16(s0)
.Ltmp1:
	.loc	1 9 9                           # main.c:9:9
	bge	a0, a1, .LBB0_2
	j	.LBB0_1
.LBB0_1:
.Ltmp2:
	.loc	1 10 17 is_stmt 1               # main.c:10:17
	lw	a0, -12(s0)
	.loc	1 10 23 is_stmt 0               # main.c:10:23
	ori	a0, a0, 256
	.loc	1 10 15                         # main.c:10:15
	sw	a0, -12(s0)
	.loc	1 10 9                          # main.c:10:9
	j	.LBB0_2
.Ltmp3:
.LBB0_2:
	.loc	1 11 12 is_stmt 1               # main.c:11:12
	lw	a0, -12(s0)
	lw	ra, 12(sp)                      # 4-byte Folded Reload
	lw	s0, 8(sp)                       # 4-byte Folded Reload
	.loc	1 11 5 epilogue_begin is_stmt 0 # main.c:11:5
	addi	sp, sp, 16
	ret
.Ltmp4:
.Lfunc_end0:
	.size	mark_below, .Lfunc_end0-mark_below
	.cfi_endproc
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	2
	.type	main,@function
main:                                   # @main
.Lfunc_begin1:
	.loc	1 15 0 is_stmt 1                # main.c:15:0
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -48
	.cfi_def_cfa_offset 48
	sw	ra, 44(sp)                      # 4-byte Folded Spill
	sw	s0, 40(sp)                      # 4-byte Folded Spill
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	addi	s0, sp, 48
	.cfi_def_cfa s0, 0
	lui	a0, 300
	addi	a0, a0, 1206
.Ltmp5:
	.loc	1 16 18 prologue_end            # main.c:16:18
	sw	a0, -12(s0)
	li	a0, 0
	.loc	1 17 12                         # main.c:17:12
	sw	a0, -20(s0)
	li	a1, 56
	.loc	1 17 21 is_stmt 0               # main.c:17:21
	sw	a1, -24(s0)
.Ltmp6:
	.loc	1 18 12 is_stmt 1               # main.c:18:12
	sw	a0, -16(s0)
	.loc	1 18 10 is_stmt 0               # main.c:18:10
	j	.LBB1_1
.LBB1_1:                                # =>This Inner Loop Header: Depth=1
.Ltmp7:
	.loc	1 18 17                         # main.c:18:17
	lw	a1, -16(s0)
	li	a0, 29
.Ltmp8:
	.loc	1 18 5                          # main.c:18:5
	blt	a0, a1, .LBB1_4
	j	.LBB1_2
.LBB1_2:                                #   in Loop: Header=BB1_1 Depth=1
.Ltmp9:
	.loc	1 19 24 is_stmt 1               # main.c:19:24
	lw	a0, -12(s0)
	lui	a1, 406
	addi	a1, a1, 1549
	.loc	1 19 22 is_stmt 0               # main.c:19:22
	mul	a0, a0, a1
	lui	a1, 247535
	addi	a1, a1, 863
	.loc	1 19 26                         # main.c:19:26
	add	a0, a0, a1
	.loc	1 19 11                         # main.c:19:11
	sw	a0, -12(s0)
	.loc	1 20 28 is_stmt 1               # main.c:20:28
	lw	a0, -12(s0)
	.loc	1 20 30 is_stmt 0               # main.c:20:30
	srli	a0, a0, 16
	lui	a1, 10382
	addi	a1, a1, -243
	.loc	1 20 37                         # main.c:20:37
	mulhu	a1, a0, a1
	li	a2, 101
	mul	a1, a1, a2
	sub	a0, a0, a1
	.loc	1 20 16                         # main.c:20:16
	lw	a2, -16(s0)
	.loc	1 20 9                          # main.c:20:9
	lui	a1, %hi(grades)
	addi	a1, a1, %lo(grades)
	slli	a2, a2, 2
	add	a1, a1, a2
	.loc	1 20 19                         # main.c:20:19
	sw	a0, 0(a1)
	.loc	1 21 5 is_stmt 1                # main.c:21:5
	j	.LBB1_3
.Ltmp10:
.LBB1_3:                                #   in Loop: Header=BB1_1 Depth=1
	.loc	1 18 25                         # main.c:18:25
	lw	a0, -16(s0)
	addi	a0, a0, 1
	sw	a0, -16(s0)
	.loc	1 18 5 is_stmt 0                # main.c:18:5
	j	.LBB1_1
.Ltmp11:
.LBB1_4:
	.loc	1 0 5                           # main.c:0:5
	li	a0, 0
.Ltmp12:
	.loc	1 22 12 is_stmt 1               # main.c:22:12
	sw	a0, -16(s0)
	.loc	1 22 10 is_stmt 0               # main.c:22:10
	j	.LBB1_5
.LBB1_5:                                # =>This Inner Loop Header: Depth=1
.Ltmp13:
	.loc	1 22 17                         # main.c:22:17
	lw	a1, -16(s0)
	li	a0, 29
.Ltmp14:
	.loc	1 22 5                          # main.c:22:5
	blt	a0, a1, .LBB1_22
	j	.LBB1_6
.LBB1_6:                                #   in Loop: Header=BB1_5 Depth=1
.Ltmp15:
	.loc	1 23 24 is_stmt 1               # main.c:23:24
	lw	a0, -16(s0)
	.loc	1 23 17 is_stmt 0               # main.c:23:17
	slli	a1, a0, 2
	lui	a0, %hi(grades)
	addi	a0, a0, %lo(grades)
	add	a0, a0, a1
	lw	a0, 0(a0)
	.loc	1 23 13                         # main.c:23:13
	sw	a0, -28(s0)
	.loc	1 24 15 is_stmt 1               # main.c:24:15
	lw	a0, -20(s0)
	.loc	1 24 21 is_stmt 0               # main.c:24:21
	lw	a1, -28(s0)
	.loc	1 24 19                         # main.c:24:19
	add	a0, a0, a1
	.loc	1 24 13                         # main.c:24:13
	sw	a0, -20(s0)
.Ltmp16:
	.loc	1 25 13 is_stmt 1               # main.c:25:13
	lw	a1, -28(s0)
	li	a0, 49
.Ltmp17:
	.loc	1 25 13 is_stmt 0               # main.c:25:13
	blt	a0, a1, .LBB1_8
	j	.LBB1_7
.LBB1_7:                                #   in Loop: Header=BB1_5 Depth=1
.Ltmp18:
	.loc	1 25 30                         # main.c:25:30
	lui	a1, %hi(bucket)
	lw	a0, %lo(bucket)(a1)
	addi	a0, a0, 1
	sw	a0, %lo(bucket)(a1)
	.loc	1 25 21                         # main.c:25:21
	j	.LBB1_18
.LBB1_8:                                #   in Loop: Header=BB1_5 Depth=1
.Ltmp19:
	.loc	1 26 18 is_stmt 1               # main.c:26:18
	lw	a1, -28(s0)
	li	a0, 64
.Ltmp20:
	.loc	1 26 18 is_stmt 0               # main.c:26:18
	blt	a0, a1, .LBB1_10
	j	.LBB1_9
.LBB1_9:                                #   in Loop: Header=BB1_5 Depth=1
.Ltmp21:
	.loc	1 26 35                         # main.c:26:35
	lui	a0, %hi(bucket)
	addi	a1, a0, %lo(bucket)
	lw	a0, 4(a1)
	addi	a0, a0, 1
	sw	a0, 4(a1)
	.loc	1 26 26                         # main.c:26:26
	j	.LBB1_17
.LBB1_10:                               #   in Loop: Header=BB1_5 Depth=1
.Ltmp22:
	.loc	1 27 18 is_stmt 1               # main.c:27:18
	lw	a1, -28(s0)
	li	a0, 74
.Ltmp23:
	.loc	1 27 18 is_stmt 0               # main.c:27:18
	blt	a0, a1, .LBB1_12
	j	.LBB1_11
.LBB1_11:                               #   in Loop: Header=BB1_5 Depth=1
.Ltmp24:
	.loc	1 27 35                         # main.c:27:35
	lui	a0, %hi(bucket)
	addi	a1, a0, %lo(bucket)
	lw	a0, 8(a1)
	addi	a0, a0, 1
	sw	a0, 8(a1)
	.loc	1 27 26                         # main.c:27:26
	j	.LBB1_16
.LBB1_12:                               #   in Loop: Header=BB1_5 Depth=1
.Ltmp25:
	.loc	1 28 18 is_stmt 1               # main.c:28:18
	lw	a1, -28(s0)
	li	a0, 84
.Ltmp26:
	.loc	1 28 18 is_stmt 0               # main.c:28:18
	blt	a0, a1, .LBB1_14
	j	.LBB1_13
.LBB1_13:                               #   in Loop: Header=BB1_5 Depth=1
.Ltmp27:
	.loc	1 28 35                         # main.c:28:35
	lui	a0, %hi(bucket)
	addi	a1, a0, %lo(bucket)
	lw	a0, 12(a1)
	addi	a0, a0, 1
	sw	a0, 12(a1)
	.loc	1 28 26                         # main.c:28:26
	j	.LBB1_15
.LBB1_14:                               #   in Loop: Header=BB1_5 Depth=1
	.loc	1 29 23 is_stmt 1               # main.c:29:23
	lui	a0, %hi(bucket)
	addi	a1, a0, %lo(bucket)
	lw	a0, 16(a1)
	addi	a0, a0, 1
	sw	a0, 16(a1)
	j	.LBB1_15
.Ltmp28:
.LBB1_15:                               #   in Loop: Header=BB1_5 Depth=1
	.loc	1 0 23 is_stmt 0                # main.c:0:23
	j	.LBB1_16
.LBB1_16:                               #   in Loop: Header=BB1_5 Depth=1
	j	.LBB1_17
.LBB1_17:                               #   in Loop: Header=BB1_5 Depth=1
	j	.LBB1_18
.LBB1_18:                               #   in Loop: Header=BB1_5 Depth=1
.Ltmp29:
	.loc	1 30 13 is_stmt 1               # main.c:30:13
	lw	a0, -28(s0)
	.loc	1 30 18 is_stmt 0               # main.c:30:18
	lw	a1, -24(s0)
.Ltmp30:
	.loc	1 30 13                         # main.c:30:13
	blt	a0, a1, .LBB1_20
	j	.LBB1_19
.LBB1_19:                               #   in Loop: Header=BB1_5 Depth=1
.Ltmp31:
	.loc	1 30 34                         # main.c:30:34
	lui	a1, %hi(pass_count)
	lw	a0, %lo(pass_count)(a1)
	addi	a0, a0, 1
	sw	a0, %lo(pass_count)(a1)
	.loc	1 30 24                         # main.c:30:24
	j	.LBB1_20
.Ltmp32:
.LBB1_20:                               #   in Loop: Header=BB1_5 Depth=1
	.loc	1 31 5 is_stmt 1                # main.c:31:5
	j	.LBB1_21
.Ltmp33:
.LBB1_21:                               #   in Loop: Header=BB1_5 Depth=1
	.loc	1 22 25                         # main.c:22:25
	lw	a0, -16(s0)
	addi	a0, a0, 1
	sw	a0, -16(s0)
	.loc	1 22 5 is_stmt 0                # main.c:22:5
	j	.LBB1_5
.Ltmp34:
.LBB1_22:
	.loc	1 32 12 is_stmt 1               # main.c:32:12
	lw	a1, -20(s0)
	lui	a0, 559241
	addi	a0, a0, -1911
	.loc	1 32 16 is_stmt 0               # main.c:32:16
	mulh	a0, a1, a0
	add	a0, a0, a1
	srli	a1, a0, 31
	srai	a0, a0, 4
	add	a0, a0, a1
	.loc	1 32 10                         # main.c:32:10
	lui	a1, %hi(mean)
	sw	a0, %lo(mean)(a1)
	li	a0, 0
.Ltmp35:
	.loc	1 33 12 is_stmt 1               # main.c:33:12
	sw	a0, -16(s0)
	.loc	1 33 10 is_stmt 0               # main.c:33:10
	j	.LBB1_23
.LBB1_23:                               # =>This Inner Loop Header: Depth=1
.Ltmp36:
	.loc	1 33 17                         # main.c:33:17
	lw	a1, -16(s0)
	li	a0, 29
.Ltmp37:
	.loc	1 33 5                          # main.c:33:5
	blt	a0, a1, .LBB1_28
	j	.LBB1_24
.LBB1_24:                               #   in Loop: Header=BB1_23 Depth=1
.Ltmp38:
	.loc	1 34 24 is_stmt 1               # main.c:34:24
	lw	a0, -16(s0)
	.loc	1 34 17 is_stmt 0               # main.c:34:17
	slli	a1, a0, 2
	lui	a0, %hi(grades)
	addi	a0, a0, %lo(grades)
	sw	a0, -36(s0)                     # 4-byte Folded Spill
	add	a0, a0, a1
	lw	a0, 0(a0)
	.loc	1 34 13                         # main.c:34:13
	sw	a0, -32(s0)
	.loc	1 35 32 is_stmt 1               # main.c:35:32
	lw	a0, -32(s0)
	.loc	1 35 35 is_stmt 0               # main.c:35:35
	lui	a1, %hi(mean)
	lw	a1, %lo(mean)(a1)
	.loc	1 35 21                         # main.c:35:21
	call	mark_below
	mv	a1, a0
	lw	a0, -36(s0)                     # 4-byte Folded Reload
	.loc	1 35 16                         # main.c:35:16
	lw	a2, -16(s0)
	.loc	1 35 9                          # main.c:35:9
	slli	a2, a2, 2
	add	a2, a0, a2
	.loc	1 35 19                         # main.c:35:19
	sw	a1, 0(a2)
.Ltmp39:
	.loc	1 36 20 is_stmt 1               # main.c:36:20
	lw	a1, -16(s0)
	.loc	1 36 13 is_stmt 0               # main.c:36:13
	slli	a1, a1, 2
	add	a0, a0, a1
	.loc	1 36 23                         # main.c:36:23
	lbu	a0, 1(a0)
	andi	a0, a0, 1
.Ltmp40:
	.loc	1 36 13                         # main.c:36:13
	beqz	a0, .LBB1_26
	j	.LBB1_25
.LBB1_25:                               #   in Loop: Header=BB1_23 Depth=1
.Ltmp41:
	.loc	1 36 43                         # main.c:36:43
	lui	a1, %hi(below_count)
	lw	a0, %lo(below_count)(a1)
	addi	a0, a0, 1
	sw	a0, %lo(below_count)(a1)
	.loc	1 36 32                         # main.c:36:32
	j	.LBB1_26
.Ltmp42:
.LBB1_26:                               #   in Loop: Header=BB1_23 Depth=1
	.loc	1 37 5 is_stmt 1                # main.c:37:5
	j	.LBB1_27
.Ltmp43:
.LBB1_27:                               #   in Loop: Header=BB1_23 Depth=1
	.loc	1 33 25                         # main.c:33:25
	lw	a0, -16(s0)
	addi	a0, a0, 1
	sw	a0, -16(s0)
	.loc	1 33 5 is_stmt 0                # main.c:33:5
	j	.LBB1_23
.Ltmp44:
.LBB1_28:
	.loc	1 0 5                           # main.c:0:5
	li	a0, 0
	lw	ra, 44(sp)                      # 4-byte Folded Reload
	lw	s0, 40(sp)                      # 4-byte Folded Reload
	.loc	1 38 5 epilogue_begin is_stmt 1 # main.c:38:5
	addi	sp, sp, 48
	ret
.Ltmp45:
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
	.byte	11                              # Abbreviation Code
	.byte	5                               # DW_TAG_formal_parameter
	.byte	0                               # DW_CHILDREN_no
	.byte	2                               # DW_AT_location
	.byte	24                              # DW_FORM_exprloc
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
	.byte	12                              # Abbreviation Code
	.byte	52                              # DW_TAG_variable
	.byte	0                               # DW_CHILDREN_no
	.byte	2                               # DW_AT_location
	.byte	24                              # DW_FORM_exprloc
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
	.byte	13                              # Abbreviation Code
	.byte	11                              # DW_TAG_lexical_block
	.byte	1                               # DW_CHILDREN_yes
	.byte	17                              # DW_AT_low_pc
	.byte	1                               # DW_FORM_addr
	.byte	18                              # DW_AT_high_pc
	.byte	6                               # DW_FORM_data4
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
	.byte	1                               # Abbrev [1] 0xb:0x173 DW_TAG_compile_unit
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
	.byte	10                              # Abbrev [10] 0xcd:0x32 DW_TAG_subprogram
	.word	.Lfunc_begin0                   # DW_AT_low_pc
	.word	.Lfunc_end0-.Lfunc_begin0       # DW_AT_high_pc
	.byte	1                               # DW_AT_frame_base
	.byte	88
	.word	.Linfo_string13                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	7                               # DW_AT_decl_line
                                        # DW_AT_prototyped
	.word	60                              # DW_AT_type
                                        # DW_AT_external
	.byte	11                              # Abbrev [11] 0xe2:0xe DW_TAG_formal_parameter
	.byte	2                               # DW_AT_location
	.byte	145
	.byte	116
	.word	.Linfo_string15                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	7                               # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	11                              # Abbrev [11] 0xf0:0xe DW_TAG_formal_parameter
	.byte	2                               # DW_AT_location
	.byte	145
	.byte	112
	.word	.Linfo_string16                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	7                               # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	0                               # End Of Children Mark
	.byte	10                              # Abbrev [10] 0xff:0x7e DW_TAG_subprogram
	.word	.Lfunc_begin1                   # DW_AT_low_pc
	.word	.Lfunc_end1-.Lfunc_begin1       # DW_AT_high_pc
	.byte	1                               # DW_AT_frame_base
	.byte	88
	.word	.Linfo_string14                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	14                              # DW_AT_decl_line
                                        # DW_AT_prototyped
	.word	60                              # DW_AT_type
                                        # DW_AT_external
	.byte	12                              # Abbrev [12] 0x114:0xe DW_TAG_variable
	.byte	2                               # DW_AT_location
	.byte	145
	.byte	116
	.word	.Linfo_string17                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	16                              # DW_AT_decl_line
	.word	198                             # DW_AT_type
	.byte	12                              # Abbrev [12] 0x122:0xe DW_TAG_variable
	.byte	2                               # DW_AT_location
	.byte	145
	.byte	112
	.word	.Linfo_string18                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	17                              # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	12                              # Abbrev [12] 0x130:0xe DW_TAG_variable
	.byte	2                               # DW_AT_location
	.byte	145
	.byte	108
	.word	.Linfo_string19                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	17                              # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	12                              # Abbrev [12] 0x13e:0xe DW_TAG_variable
	.byte	2                               # DW_AT_location
	.byte	145
	.byte	104
	.word	.Linfo_string20                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	17                              # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	13                              # Abbrev [13] 0x14c:0x18 DW_TAG_lexical_block
	.word	.Ltmp15                         # DW_AT_low_pc
	.word	.Ltmp33-.Ltmp15                 # DW_AT_high_pc
	.byte	12                              # Abbrev [12] 0x155:0xe DW_TAG_variable
	.byte	2                               # DW_AT_location
	.byte	145
	.byte	100
	.word	.Linfo_string21                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	23                              # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	0                               # End Of Children Mark
	.byte	13                              # Abbrev [13] 0x164:0x18 DW_TAG_lexical_block
	.word	.Ltmp38                         # DW_AT_low_pc
	.word	.Ltmp43-.Ltmp38                 # DW_AT_high_pc
	.byte	12                              # Abbrev [12] 0x16d:0xe DW_TAG_variable
	.byte	2                               # DW_AT_location
	.byte	145
	.byte	96
	.word	.Linfo_string21                 # DW_AT_name
	.byte	1                               # DW_AT_decl_file
	.byte	34                              # DW_AT_decl_line
	.word	60                              # DW_AT_type
	.byte	0                               # End Of Children Mark
	.byte	0                               # End Of Children Mark
	.byte	0                               # End Of Children Mark
.Ldebug_info_end0:
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
	.asciz	"main"                          # string offset=261
.Linfo_string15:
	.asciz	"value"                         # string offset=266
.Linfo_string16:
	.asciz	"average"                       # string offset=272
.Linfo_string17:
	.asciz	"x"                             # string offset=280
.Linfo_string18:
	.asciz	"i"                             # string offset=282
.Linfo_string19:
	.asciz	"sum"                           # string offset=284
.Linfo_string20:
	.asciz	"pass"                          # string offset=288
.Linfo_string21:
	.asciz	"v"                             # string offset=293
	.ident	"clang version 18.1.6 (https://github.com/ziglang/zig-bootstrap 98bc6bf4fc4009888d33941daf6b600d20a42a56)"
	.section	".note.GNU-stack","",@progbits
	.addrsig
	.addrsig_sym mark_below
	.addrsig_sym grades
	.addrsig_sym bucket
	.addrsig_sym pass_count
	.addrsig_sym mean
	.addrsig_sym below_count
	.section	.debug_line,"",@progbits
.Lline_table_start0:
