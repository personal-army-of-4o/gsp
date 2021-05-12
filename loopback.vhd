library ieee;
use ieee.std_logic_1164.all;

entity logic_top is
    port (
        iClk: in std_logic;
        iReset: in std_logic;

        iRs_dbg: in std_logic;
        oRs_dbg: out std_logic
    );
end entity;

architecture v1 of logic_top is
begin

    oRs_dbg <= iRs_dbg;

end v1;
