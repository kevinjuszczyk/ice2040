/*
 ------------------------------------------------------------------------------
| Copyright (C) 2022 Kevin Juszczyk                                            |
|                                                                              |
| This source describes Open Hardware and is licensed under the CERN-OHL-S v2. |
|                                                                              |
| You may redistribute and modify this source and make products using it under |
| the terms of the CERN-OHL-S v2 (https://ohwr.org/cern_ohl_s_v2.txt).         |
|                                                                              |
| This source is distributed WITHOUT ANY EXPRESS OR IMPLIED WARRANTY,          |
| INCLUDING OF MERCHANTABILITY, SATISFACTORY QUALITY AND FITNESS FOR A         |
| PARTICULAR PURPOSE. Please see the CERN-OHL-S v2 for applicable conditions.  |
|                                                                              |
| Source location: https://github.com/kevinjuszczyk/ice2040                    |
|                                                                              |
| As per CERN-OHL-S v2 section 4, should You produce hardware based on this    |
| source, You must where practicable maintain the Source Location visible      |
| on the external case of the ICE2040 or other products you make using this    |
| source.                                                                      |
 ------------------------------------------------------------------------------
*/

module top(
           input  CLK,
           input  P1A9,
           input  P1A4,
           output P1A7,
           output P1A1,
           output P1A2,
           output P1A3,
           output P1A8
           );

   assign {P1A7, P1A1, P1A2, P1A3, P1A8} = leds;

   // CLK = 12 MHz
   reg [25:0]     counter;

   // P1A7 ~ 0.16Hz, P1A1 ~ 0.35Hz, P1A2 ~ 0.7Hz, P1A3 ~ 1.4Hz, P1A8 ~ 2.8Hz
   wire [4:0]     leds = counter[21+:5];

   always @(posedge CLK) begin
      counter <= counter + 1;
   end

endmodule // top
