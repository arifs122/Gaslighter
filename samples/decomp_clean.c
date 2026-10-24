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



/* build_target @ 00101169 */

void build_target(undefined1 *param_1)

{
  *param_1 = 0x68;
  param_1[1] = 0x74;
  param_1[2] = 0x74;
  param_1[3] = 0x70;
  param_1[4] = 0x3a;
  param_1[5] = 0x2f;
  param_1[6] = 0x2f;
  param_1[7] = 0x31;
  param_1[8] = 0x39;
  param_1[9] = 0x32;
  param_1[10] = 0x2e;
  param_1[0xb] = 0x30;
  param_1[0xc] = 0x2e;
  param_1[0xd] = 0x32;
  param_1[0xe] = 0x2e;
  param_1[0xf] = 0x31;
  param_1[0x10] = 0x3a;
  param_1[0x11] = 0x34;
  param_1[0x12] = 0x34;
  param_1[0x13] = 0x34;
  param_1[0x14] = 0x34;
  param_1[0x15] = 0x2f;
  param_1[0x16] = 0x67;
  param_1[0x17] = 0x61;
  param_1[0x18] = 0x74;
  param_1[0x19] = 0x65;
  param_1[0x1a] = 0x2e;
  param_1[0x1b] = 0x70;
  param_1[0x1c] = 0x68;
  param_1[0x1d] = 0x70;
  param_1[0x1e] = 0;
  return;
}



/* main @ 001012c9 */

undefined8 main(void)

{
  long in_FS_OFFSET;
  undefined1 local_58 [72];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  build_target(local_58);
  printf("connecting to %s\n",local_58);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}



/* ===== STRINGS (analist gorunumu) ===== */
/lib64/ld-linux-x86-64.so.2
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
sample_clean.c
build_target
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