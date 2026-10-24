/* FUN_00101020 @ 00101020 */

void FUN_00101020(void)

{
  (*(code *)PTR_00103fa0)();
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
  printf("connecting to %s\n","http://192.0.2.1:4444/gate.php");
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}



/* main @ 0010128c */

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
192.0.2.1
http://192.0.2.1:4444/gate.php
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
sample_ev_flood.c
beacon
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