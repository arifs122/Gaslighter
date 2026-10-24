/* FUN_00101020 @ 00101020 */

void FUN_00101020(void)

{
  (*(code *)PTR_00103f98)();
  return;
}



/* deregister_tm_clones @ 00101150 */

/* WARNING: Removing unreachable block (ram,0x00101163) */
/* WARNING: Removing unreachable block (ram,0x0010116f) */

void deregister_tm_clones(void)

{
  return;
}



/* register_tm_clones @ 00101180 */

/* WARNING: Removing unreachable block (ram,0x001011a4) */
/* WARNING: Removing unreachable block (ram,0x001011b0) */

void register_tm_clones(void)

{
  return;
}



/* opaque @ 00101209 */

bool opaque(int param_1)

{
  return (param_1 + param_1 * param_1 & 1U) == 0;
}



/* init_config @ 0010122e */

int init_config(int param_1)

{
  return param_1 + 1;
}



/* read_config @ 00101241 */

int read_config(int param_1)

{
  return param_1 * 2;
}



/* log_event @ 00101253 */

int log_event(int param_1)

{
  return param_1 + -1;
}



/* checksum @ 00101266 */

uint checksum(uint param_1)

{
  return param_1 ^ 0x55;
}



/* cleanup @ 00101279 */

void cleanup(EVP_PKEY_CTX *ctx)

{
  return;
}



/* run_task @ 0010128c */

int run_task(int param_1)

{
  return param_1 + 7;
}



/* process_data @ 0010129f */

void process_data(void)

{
  long in_FS_OFFSET;
  int local_e0;
  undefined2 local_d8;
  uint16_t local_d6;
  in_addr_t local_d4;
  byte local_c1 [41];
  byte local_98 [9];
  undefined1 local_8f;
  byte local_78 [30];
  undefined1 local_5a;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_c1[0] = 0x6b;
  local_c1[1] = 99;
  local_c1[2] = 0x68;
  local_c1[3] = 0x74;
  local_c1[4] = 0x6a;
  local_c1[5] = 0x74;
  local_c1[6] = 0x68;
  local_c1[7] = 0x74;
  local_c1[8] = 0x6b;
  local_c1[9] = 0x32;
  local_c1[10] = 0x2e;
  local_c1[0xb] = 0x2e;
  local_c1[0xc] = 0x2a;
  local_c1[0xd] = 0x60;
  local_c1[0xe] = 0x75;
  local_c1[0xf] = 0x75;
  local_c1[0x10] = 0x6b;
  local_c1[0x11] = 99;
  local_c1[0x12] = 0x68;
  local_c1[0x13] = 0x74;
  local_c1[0x14] = 0x6a;
  local_c1[0x15] = 0x74;
  local_c1[0x16] = 0x68;
  local_c1[0x17] = 0x74;
  local_c1[0x18] = 0x6b;
  local_c1[0x19] = 0x60;
  local_c1[0x1a] = 0x6e;
  local_c1[0x1b] = 0x6e;
  local_c1[0x1c] = 0x6e;
  local_c1[0x1d] = 0x6e;
  local_c1[0x1e] = 0x75;
  local_c1[0x1f] = 0x3d;
  local_c1[0x20] = 0x3b;
  local_c1[0x21] = 0x2e;
  local_c1[0x22] = 0x3f;
  local_c1[0x23] = 0x74;
  local_c1[0x24] = 0x2a;
  local_c1[0x25] = 0x32;
  local_c1[0x26] = 0x2a;
  for (local_e0 = 0; local_e0 < 9; local_e0 = local_e0 + 1) {
    local_98[local_e0] = local_c1[local_e0] ^ 0x5a;
  }
  local_8f = 0;
  for (local_e0 = 0; local_e0 < 0x1e; local_e0 = local_e0 + 1) {
    local_78[local_e0] = local_c1[(long)local_e0 + 9] ^ 0x5a;
  }
  local_5a = 0;
  socket(2,1,0);
  memset(&local_d8,0,0x10);
  local_d8 = 2;
  local_d6 = htons(0x115c);
  local_d4 = inet_addr((char *)local_98);
  printf("connecting to %s\n",local_78);
  puts("Build note: this sample was compiled for a test.");
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}



/* main @ 00101444 */

undefined8 main(void)

{
  int iVar1;
  
  process_data();
  init_config(1);
  read_config(2);
  log_event(3);
  checksum(4);
  cleanup((EVP_PKEY_CTX *)0x5);
  run_task(6);
  iVar1 = opaque(7);
  if (iVar1 == 0) {
    puts("no");
  }
  else {
    puts("ok");
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
__cxa_finalize
memset
printf
libc.so.6
GLIBC_2.4
GLIBC_2.2.5
GLIBC_2.34
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
kchtjthtH
2..*`uukH
chtjthtkH
tk`nnnnuH
=;.?t*2*H
connecting to %s
Build note: this sample was compiled for a test.
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
sample_mut_combo.c
opaque
init_config
read_config
log_event
checksum
cleanup
run_task
process_data
__FRAME_END__
_DYNAMIC
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
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