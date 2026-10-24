/* FUN_00101020 @ 00101020 */

void FUN_00101020(void)

{
  (*(code *)PTR_00103fc0)();
  return;
}



/* deregister_tm_clones @ 001010b0 */

/* WARNING: Removing unreachable block (ram,0x001010c3) */
/* WARNING: Removing unreachable block (ram,0x001010cf) */

void deregister_tm_clones(void)

{
  return;
}



/* register_tm_clones @ 001010e0 */

/* WARNING: Removing unreachable block (ram,0x00101104) */
/* WARNING: Removing unreachable block (ram,0x00101110) */

void register_tm_clones(void)

{
  return;
}



/* bx @ 00101169 */

void bx(long param_1)

{
  int local_c;
  
  for (local_c = 0; local_c < 0x1e; local_c = local_c + 1) {
    *(byte *)(param_1 + local_c) = enc[local_c] ^ 0x5a;
  }
  *(undefined1 *)(param_1 + 0x1e) = 0;
  return;
}



/* opaque @ 001011c7 */

bool opaque(int param_1)

{
  return (param_1 + param_1 * param_1 & 1U) == 0;
}



/* main @ 001011ec */

undefined8 main(void)

{
  int iVar1;
  long in_FS_OFFSET;
  undefined1 local_58 [72];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  iVar1 = opaque(7);
  if (iVar1 != 0) {
    (*(code *)fp_build)(local_58);
  }
  printf("connecting to %s\n",local_58);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}



/* ===== STRINGS (analist gorunumu) ===== */
/lib64/ld-linux-x86-64.so.2
P9nyV
__stack_chk_fail
__libc_start_main
__cxa_finalize
printf
libc.so.6
GLIBC_2.2.5
GLIBC_2.4
GLIBC_2.34
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
connecting to %s
9*3$"
2..*`uukchtjthtk`nnnnu=;.?t*2*
GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
Scrt1.o
__abi_tag
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.0
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
sample_obf.c
enc_len
fp_build
opaque
__FRAME_END__
_DYNAMIC
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_start_main@GLIBC_2.34
_edata
_fini
__stack_chk_fail@GLIBC_2.4
printf@GLIBC_2.2.5
__data_start
__dso_handle
_IO_stdin_used
__bss_start
__TMC_END__
__cxa_finalize@GLIBC_2.2.5
_init
.symtab
.strtab
.shstrtab
.interp
.note.gnu.property
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.plt.sec
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.data
.comment