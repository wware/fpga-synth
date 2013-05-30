// File: fpga.v
// Generated by MyHDL 0.7
// Date: Thu May 30 00:30:01 2013


`timescale 1ns/10ps

module fpga (
    fastclk,
    reset,
    param_data,
    param_clk,
    audio_req,
    audio_ack,
    dac_bit
);


input fastclk;
input reset;
input [3:0] param_data;
input param_clk;
input audio_req;
input audio_ack;
output dac_bit;
wire dac_bit;

reg [3:0] _release;
reg [13:0] threshold;
reg [23:0] input_driver_count;
reg [1:0] select;
reg [3:0] decay;
reg [3:0] attack;
reg [3:0] sustain;
reg [9:0] aclk_counter;
reg keydown;
reg clk;
reg [23:0] delta_phase;
reg signed [13:0] wavgen_output;
wire signed [13:0] drivers_3_interp_result;
reg drivers_3_dac_bit_internal;
reg [13:0] drivers_3_interp_result_unsigned;
reg [15:0] drivers_3_vc_estimate;
reg [31:0] drivers_3_sum_of_products;
reg [13:0] drivers_3_things_4___out;
reg signed [29:0] drivers_3_things_0_interp_step;
reg signed [29:0] drivers_3_things_0_interp_data;
reg signed [13:0] drivers_3_things_0_delay_1;
wire signed [13:0] drivers_3_things_0_x;
reg [12:0] drivers_2_noise_register_13;
reg [23:0] drivers_2_phase_counter;
reg [15:0] drivers_2_noise_register_16;





always @(posedge fastclk, posedge reset) begin: FPGA_DRIVERS_0
    if (reset) begin
        aclk_counter <= 0;
        clk <= 1'b1;
    end
    else if ((aclk_counter >= 800)) begin
        aclk_counter <= 0;
        clk <= 1'b1;
    end
    else begin
        aclk_counter <= (aclk_counter + 1);
        clk <= 1'b0;
    end
end


always @(posedge clk, posedge reset) begin: FPGA_DRIVE_INPUTS
    attack <= 3;
    decay <= 5;
    sustain <= 8;
    _release <= 0;
    delta_phase <= 184549;
    select <= 1;
    threshold <= 8192;
    keydown <= 0;
    if (reset) begin
        keydown <= 0;
        input_driver_count <= 0;
    end
    else if ((input_driver_count >= (5 * 40000))) begin
        keydown <= 0;
        input_driver_count <= 0;
    end
    else if ((input_driver_count < (2 * 40000))) begin
        keydown <= 1;
        input_driver_count <= (input_driver_count + 1);
    end
    else begin
        keydown <= 0;
        input_driver_count <= (input_driver_count + 1);
    end
end


always @(posedge clk, posedge reset) begin: FPGA_DRIVERS_2_WAVEFORMS
    if (reset) begin
        drivers_2_noise_register_16 <= 123;
        drivers_2_noise_register_13 <= 1787;
        drivers_2_phase_counter <= 0;
        wavgen_output <= 0;
    end
    else begin
        if ((drivers_2_noise_register_16 == 0)) begin
            drivers_2_noise_register_16 <= 123;
        end
        else if (((((drivers_2_noise_register_16 ^ (drivers_2_noise_register_16 >>> 2)) ^ (drivers_2_noise_register_16 >>> 3)) ^ (drivers_2_noise_register_16 >>> 5)) & 1)) begin
            drivers_2_noise_register_16 <= ((1 << 15) + (drivers_2_noise_register_16 >>> 1));
        end
        else begin
            drivers_2_noise_register_16 <= (drivers_2_noise_register_16 >>> 1);
        end
        if ((drivers_2_noise_register_13 == 0)) begin
            drivers_2_noise_register_13 <= 1787;
        end
        else if (((((drivers_2_noise_register_13 ^ (drivers_2_noise_register_13 >>> 1)) ^ (drivers_2_noise_register_13 >>> 2)) ^ (drivers_2_noise_register_13 >>> 5)) & 1)) begin
            drivers_2_noise_register_13 <= ((1 << 12) + (drivers_2_noise_register_13 >>> 1));
        end
        else begin
            drivers_2_noise_register_13 <= (drivers_2_noise_register_13 >>> 1);
        end
        if (((drivers_2_phase_counter + delta_phase) >= (1 << 24))) begin
            drivers_2_phase_counter <= ((drivers_2_phase_counter + delta_phase) - (1 << 24));
        end
        else begin
            drivers_2_phase_counter <= (drivers_2_phase_counter + delta_phase);
        end
        case (select)
            'h0: begin
                wavgen_output <= ((drivers_2_phase_counter - 8388608) >>> 10);
            end
            'h1: begin
                if ((drivers_2_phase_counter < 8388608)) begin
                    wavgen_output <= ((drivers_2_phase_counter - 4194304) >>> 9);
                end
                else begin
                    wavgen_output <= ((12582912 - drivers_2_phase_counter) >>> 9);
                end
            end
            'h2: begin
                if ((drivers_2_phase_counter > (threshold << (24 - 14)))) begin
                    wavgen_output <= (16383 - 8192);
                end
                else begin
                    wavgen_output <= (-8192);
                end
            end
            default: begin
                wavgen_output <= (((drivers_2_noise_register_16 ^ drivers_2_noise_register_13) & 16383) - 8192);
            end
        endcase
    end
end


always @(posedge fastclk, posedge reset) begin: FPGA_DRIVERS_3_THINGS_0_DO_STUFF
    if (reset) begin
        drivers_3_things_0_delay_1 <= 0;
        drivers_3_things_0_interp_data <= 0;
        drivers_3_things_0_interp_step <= 0;
    end
    else begin
        if (clk) begin
            drivers_3_things_0_interp_data <= (drivers_3_things_0_delay_1 << 16);
            drivers_3_things_0_delay_1 <= wavgen_output;
            drivers_3_things_0_interp_step <= ((((((((drivers_3_things_0_x << 12) + (drivers_3_things_0_x << 10)) + (drivers_3_things_0_x << 6)) + (drivers_3_things_0_x << 5)) + (drivers_3_things_0_x << 4)) + (drivers_3_things_0_x << 3)) + (drivers_3_things_0_x << 1)) + drivers_3_things_0_x);
        end
        else if (((drivers_3_things_0_interp_data + drivers_3_things_0_interp_step) < -536870912)) begin
            drivers_3_things_0_interp_data <= -536870912;
        end
        else if (((drivers_3_things_0_interp_data + drivers_3_things_0_interp_step) >= 536870912)) begin
            drivers_3_things_0_interp_data <= (536870912 - 1);
        end
        else begin
            drivers_3_things_0_interp_data <= (drivers_3_things_0_interp_data + drivers_3_things_0_interp_step);
        end
    end
end



assign drivers_3_things_0_x = (wavgen_output - drivers_3_things_0_delay_1);
assign drivers_3_interp_result = $signed(drivers_3_things_0_interp_data >>> 16);



assign dac_bit = drivers_3_dac_bit_internal;


always @(posedge fastclk, posedge reset) begin: FPGA_DRIVERS_3_DO_STUFF
    if (reset) begin
        drivers_3_dac_bit_internal <= 0;
        drivers_3_vc_estimate <= (1 << 15);
    end
    else begin
        drivers_3_dac_bit_internal <= (drivers_3_interp_result_unsigned > (drivers_3_sum_of_products >>> (32 - 14)));
        drivers_3_vc_estimate <= (drivers_3_sum_of_products >>> 16);
    end
end


always @(drivers_3_dac_bit_internal, drivers_3_vc_estimate) begin: FPGA_DRIVERS_3_MULTIPLY
    if (drivers_3_dac_bit_internal) begin
        if (((13400823 + (65332 * drivers_3_vc_estimate)) >= (1 << 32))) begin
            drivers_3_sum_of_products = ((1 << 32) - 1);
        end
        else begin
            drivers_3_sum_of_products = (13400823 + (65332 * drivers_3_vc_estimate));
        end
    end
    else begin
        drivers_3_sum_of_products = (65332 * drivers_3_vc_estimate);
    end
end


always @(drivers_3_interp_result) begin: FPGA_DRIVERS_3_THINGS_4_DRIVE__OUT
    drivers_3_things_4___out <= (drivers_3_interp_result + (1 << (14 - 1)));
end


always @(drivers_3_things_4___out) begin: FPGA_DRIVERS_3_THINGS_4_DRIVE_OUT
    drivers_3_interp_result_unsigned <= drivers_3_things_4___out;
end

endmodule
