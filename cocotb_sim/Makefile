SIM ?= ghdl
SIM_ARGS ?= --wave=waveform.ghw
TOPLEVEL_LANG ?= vhdl


VHDL_SOURCES_grlib += ../grlib/lib/grlib/stdlib/version.vhd
VHDL_SOURCES_grlib += ../grlib/lib/grlib/stdlib/stdlib.vhd
VHDL_SOURCES_grlib += ../grlib/lib/grlib/stdlib/config_types.vhd
VHDL_SOURCES_grlib += ../grlib/lib/grlib/stdlib/config.vhd
VHDL_SOURCES_grlib += ../grlib/lib/grlib/stdlib/stdio.vhd
VHDL_SOURCES_grlib += ../grlib/lib/grlib/stdlib/testlib.vhd
VHDL_SOURCES_grlib += ../grlib/lib/grlib/amba/amba.vhd
VHDL_SOURCES_grlib += ../grlib/lib/grlib/amba/devices.vhd
VHDL_SOURCES_grlib += ../grlib/lib/grlib/amba/ahbctrl.vhd
VHDL_SOURCES_grlib += ../grlib/lib/grlib/amba/ahbmst.vhd
VHDL_SOURCES_grlib += ../grlib/lib/grlib/amba/apbctrl.vhd
VHDL_SOURCES_grlib += ../grlib/lib/grlib/amba/apbctrlx.vhd

VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/misc/misc.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/misc/rstgen.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/misc/grgpio.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/uart/uart.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/uart/libdcom.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/uart/dcom.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/uart/dcom_uart.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/uart/ahbuart.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/uart/apbuart.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/spi/spi.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/spi/spictrlx.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/spi/spictrl.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/leon3/leon3.vhd
VHDL_SOURCES_gaisler += ../grlib/lib/gaisler/irqmp/irqmp.vhd

VHDL_SOURCES_techmap += ../grlib/lib/techmap/gencomp/netcomp.vhd
VHDL_SOURCES_techmap += ../grlib/lib/techmap/gencomp/gencomp.vhd
VHDL_SOURCES_techmap += ../grlib/lib/techmap/inferred/memory_inferred.vhd
VHDL_SOURCES_techmap += ../grlib/lib/techmap/alltech/allmem.vhd
VHDL_SOURCES_techmap += ../grlib/lib/techmap/maps/memrwcol.vhd
VHDL_SOURCES_techmap += ../grlib/lib/techmap/maps/syncram_2p.vhd

VHDL_SOURCES += ../hw_tester/src/hdl/wraps/logic_top.vhd

TOPLEVEL = logic_top

MODULE = tbc

include $(shell cocotb-config --makefiles)/Makefile.sim


