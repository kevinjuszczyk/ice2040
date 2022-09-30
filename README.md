# ICE2040
ICE40UP5K FPGA + RP2040 Hacker Board
![ice2040](./doc/ice2040.jpg)

## Overview
The ICE2040 combines a Lattice ICE40UP5K FPGA with a Raspberry Pi RP2040. The RP2040 is used to configure the ICE40 SRAM, and optionally provide a clock or host communication. Pmod connectors are provided for both the ICE40 and RP2040, with the rightmost connectors lined up in such a way that up to 16 additional lines between the ICE40 and RP2040 can be bridged together using a PCB or ribbon cable.

## Background
A friend expressed an interest in implementing a RISC-V processor using an FPGA, something like [learn-fpga](https://github.com/BrunoLevy/learn-fpga/blob/master/FemtoRV/TUTORIALS/FROM_BLINKER_TO_RISCV/README.md). Due to the ongoing parts shortage, many of the low end FPGA dev boards are either out of stock, or have moved out of the pocket change price range. With an eye toward building a board using whatever might still be in stock, I found that the major retailers have many thousands of ICE40 parts in fine pitch BGA packages. I started playing around in KiCad with the ICE40UP5K-UWG30 (30-ball 0.4mm pitch) part to see if there was a way to fan out enough of the pins to make a reasonably useful board. By modifying the shape of the pads, I was able to achieve a complete fanout that can be fabricated with JLCPCB's 4-layer process.
![ice2040footprint](./doc/ice2040footprint.png)
