/* FUN_00101020 @ 00101020 */

void FUN_00101020(void)

{
  (*(code *)PTR_00104fa0)();
  return;
}



/* deregister_tm_clones @ 00101130 */

/* WARNING: Removing unreachable block (ram,0x00101143) */
/* WARNING: Removing unreachable block (ram,0x0010114f) */

void deregister_tm_clones(void)

{
  return;
}



/* register_tm_clones @ 00101160 */

/* WARNING: Removing unreachable block (ram,0x00101184) */
/* WARNING: Removing unreachable block (ram,0x00101190) */

void register_tm_clones(void)

{
  return;
}



/* beacon @ 001011e9 */

void beacon(void)

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
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}



/* main @ 0010137f */

undefined8 main(void)

{
  beacon();
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
GLIBC_2.2.5
GLIBC_2.4
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
https://cdn.example.com/asset_00.js
https://cdn.example.com/asset_01.js
https://cdn.example.com/asset_02.js
https://cdn.example.com/asset_03.js
https://cdn.example.com/asset_04.js
https://cdn.example.com/asset_05.js
https://cdn.example.com/asset_06.js
https://cdn.example.com/asset_07.js
https://cdn.example.com/asset_08.js
https://cdn.example.com/asset_09.js
https://cdn.example.com/asset_10.js
https://cdn.example.com/asset_11.js
https://cdn.example.com/asset_12.js
https://cdn.example.com/asset_13.js
https://cdn.example.com/asset_14.js
https://cdn.example.com/asset_15.js
https://cdn.example.com/asset_16.js
https://cdn.example.com/asset_17.js
https://cdn.example.com/asset_18.js
https://cdn.example.com/asset_19.js
https://cdn.example.com/asset_20.js
https://cdn.example.com/asset_21.js
https://cdn.example.com/asset_22.js
https://cdn.example.com/asset_23.js
https://cdn.example.com/asset_24.js
https://cdn.example.com/asset_25.js
https://cdn.example.com/asset_26.js
https://cdn.example.com/asset_27.js
https://cdn.example.com/asset_28.js
https://cdn.example.com/asset_29.js
https://cdn.example.com/asset_30.js
https://cdn.example.com/asset_31.js
https://cdn.example.com/asset_32.js
https://cdn.example.com/asset_33.js
https://cdn.example.com/asset_34.js
https://cdn.example.com/asset_35.js
https://cdn.example.com/asset_36.js
https://cdn.example.com/asset_37.js
https://cdn.example.com/asset_38.js
https://cdn.example.com/asset_39.js
https://cdn.example.com/asset_40.js
https://cdn.example.com/asset_41.js
https://cdn.example.com/asset_42.js
https://cdn.example.com/asset_43.js
https://cdn.example.com/asset_44.js
https://cdn.example.com/asset_45.js
https://cdn.example.com/asset_46.js
https://cdn.example.com/asset_47.js
https://cdn.example.com/asset_48.js
https://cdn.example.com/asset_49.js
https://cdn.example.com/asset_50.js
https://cdn.example.com/asset_51.js
https://cdn.example.com/asset_52.js
https://cdn.example.com/asset_53.js
https://cdn.example.com/asset_54.js
https://cdn.example.com/asset_55.js
https://cdn.example.com/asset_56.js
https://cdn.example.com/asset_57.js
https://cdn.example.com/asset_58.js
https://cdn.example.com/asset_59.js
http://192.0.2.1:4444/gate.php
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
sample_flood_last.c
beacon
ev_10
ev_11
ev_12
ev_13
ev_14
ev_15
ev_16
ev_17
ev_18
ev_19
ev_20
ev_21
ev_22
ev_23
ev_24
ev_25
ev_26
ev_27
ev_28
ev_29
ev_30
ev_31
ev_32
ev_33
ev_34
ev_35
ev_36
ev_37
ev_38
ev_39
ev_40
ev_41
ev_42
ev_43
ev_44
ev_45
ev_46
ev_47
ev_48
ev_49
ev_50
ev_51
ev_52
ev_53
ev_54
ev_55
ev_56
ev_57
ev_58
ev_59
ev_60
__FRAME_END__
_DYNAMIC
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_start_main@GLIBC_2.34
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