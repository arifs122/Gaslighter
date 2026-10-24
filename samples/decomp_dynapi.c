/* FUN_00101020 @ 00101020 */

void FUN_00101020(void)

{
  (*(code *)PTR_00103fb0)();
  return;
}



/* deregister_tm_clones @ 001010f0 */

/* WARNING: Removing unreachable block (ram,0x00101103) */
/* WARNING: Removing unreachable block (ram,0x0010110f) */

void deregister_tm_clones(void)

{
  return;
}



/* register_tm_clones @ 00101120 */

/* WARNING: Removing unreachable block (ram,0x00101144) */
/* WARNING: Removing unreachable block (ram,0x00101150) */

void register_tm_clones(void)

{
  return;
}



/* dec @ 001011a9 */

void dec(long param_1,long param_2,int param_3)

{
  undefined4 local_c;
  
  for (local_c = 0; local_c < param_3; local_c = local_c + 1) {
    *(byte *)(param_1 + local_c) = *(byte *)(param_2 + local_c) ^ 0x5a;
  }
  *(undefined1 *)(param_1 + param_3) = 0;
  return;
}



/* main @ 0010120a */

undefined8 main(void)

{
  code *pcVar1;
  code *pcVar2;
  code *pcVar3;
  long in_FS_OFFSET;
  undefined2 local_118;
  undefined2 local_116;
  undefined4 local_114;
  undefined4 local_105;
  undefined1 local_101;
  undefined4 local_100;
  undefined2 local_fc;
  undefined8 local_fa;
  undefined1 local_f2;
  undefined8 local_f1;
  undefined1 local_e9;
  undefined1 local_e8 [16];
  undefined1 local_d8 [16];
  undefined1 local_c8 [16];
  undefined8 local_b8;
  undefined6 local_b0;
  undefined2 uStack_aa;
  undefined6 uStack_a8;
  undefined8 local_a2;
  undefined1 local_98 [32];
  undefined1 local_78 [104];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_100 = 0x31393529;
  local_fc = 0x2e3f;
  local_fa = 0x3e3e3b052e3f3433;
  local_f2 = 0x28;
  local_105 = 0x34352e32;
  local_101 = 0x29;
  local_f1 = 0x7468746a7468636b;
  local_e9 = 0x6b;
  local_b8 = 0x6b7575602a2e2e32;
  local_b0 = 0x68746a746863;
  uStack_aa = 0x6b74;
  uStack_a8 = 0x756e6e6e6e60;
  local_a2 = 0x2a322a743f2e3b3d;
  dec(local_e8,&local_100,6);
  dec(local_d8,&local_fa,9);
  dec(local_c8,&local_105,5);
  dec(local_98,&local_f1,9);
  dec(local_78,&local_b8,0x1e);
  pcVar1 = (code *)dlsym(0,local_e8);
  pcVar2 = (code *)dlsym(0,local_d8);
  pcVar3 = (code *)dlsym(0,local_c8);
  (*pcVar1)(2,1,0);
  memset(&local_118,0,0x10);
  local_118 = 2;
  local_116 = (*pcVar3)(0x115c);
  local_114 = (*pcVar2)(local_98);
  printf("connecting to %s\n",local_78);
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
dlsym
__cxa_finalize
memset
printf
libc.so.6
GLIBC_2.2.5
GLIBC_2.4
GLIBC_2.34
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
)591f
kchtjthtH
2..*`uukH
chtjthtkH
tk`nnnnuH
=;.?t*2*H
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
sample_dynapi.c
__FRAME_END__
_DYNAMIC
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_start_main@GLIBC_2.34
_edata
_fini
__stack_chk_fail@GLIBC_2.4
printf@GLIBC_2.2.5
memset@GLIBC_2.2.5
__data_start
__dso_handle
_IO_stdin_used
__bss_start
dlsym@GLIBC_2.34
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