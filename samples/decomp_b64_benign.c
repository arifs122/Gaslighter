/* FUN_00101020 @ 00101020 */

void FUN_00101020(void)

{
  (*(code *)PTR_00103f88)();
  return;
}



/* deregister_tm_clones @ 00101190 */

/* WARNING: Removing unreachable block (ram,0x001011a3) */
/* WARNING: Removing unreachable block (ram,0x001011af) */

void deregister_tm_clones(void)

{
  return;
}



/* register_tm_clones @ 001011c0 */

/* WARNING: Removing unreachable block (ram,0x001011e4) */
/* WARNING: Removing unreachable block (ram,0x001011f0) */

void register_tm_clones(void)

{
  return;
}



/* main @ 00101249 */

undefined8 main(void)

{
  char *pcVar1;
  long in_FS_OFFSET;
  undefined2 local_28;
  uint16_t local_26;
  in_addr_t local_24;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  socket(2,1,0);
  memset(&local_28,0,0x10);
  local_28 = 2;
  local_26 = htons(0x115c);
  local_24 = inet_addr("192.0.2.1");
  pcVar1 = getenv("CROWBAR_TEST_NEVER_SET_12345");
  if (pcVar1 != (char *)0x0) {
    execl("/bin/sh","sh",0);
  }
  printf("connecting to %s\n","http://192.0.2.1:4444/gate.php");
  puts(
      "QnVpbGQgbm90ZTogdGhpcyBzYW1wbGUgd2FzIGNvbXBpbGVkIGZvciBhIHRlc3Q7IGl0IHByaW50cyBhIGdyZWV0aW5nLg=="
      );
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}



/* ===== STRINGS (analist gorunumu) ===== */
/lib64/ld-linux-x86-64.so.2
inet_addr
__stack_chk_fail
htons
socket
__libc_start_main
execl
__cxa_finalize
getenv
memset
printf
libc.so.6
GLIBC_2.4
GLIBC_2.34
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
192.0.2.1
CROWBAR_TEST_NEVER_SET_12345
/bin/sh
http://192.0.2.1:4444/gate.php
connecting to %s
QnVpbGQgbm90ZTogdGhpcyBzYW1wbGUgd2FzIGNvbXBpbGVkIGZvciBhIHRlc3Q7IGl0IHByaW50cyBhIGdyZWV0aW5nLg==
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
sample_b64_benign.c
__FRAME_END__
_DYNAMIC
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
getenv@GLIBC_2.2.5
__libc_start_main@GLIBC_2.34
puts@GLIBC_2.2.5
_edata
_fini
__stack_chk_fail@GLIBC_2.4
htons@GLIBC_2.2.5
printf@GLIBC_2.2.5
memset@GLIBC_2.2.5
__data_start
inet_addr@GLIBC_2.2.5
__dso_handle
_IO_stdin_used
__bss_start
__TMC_END__
execl@GLIBC_2.2.5
__cxa_finalize@GLIBC_2.2.5
_init
socket@GLIBC_2.2.5
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