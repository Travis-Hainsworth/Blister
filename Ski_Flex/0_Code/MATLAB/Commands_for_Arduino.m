% classdef Commands_for_Arduino
%    % 
%    % methods
        function ret_mm = return_to_start(   ser)
            MOVE_TO_START = 2;
            serial_string = strcat(num2str(MOVE_TO_START),",0,1");
            ret_mm = serial_communication( ser, serial_string);
            flush(ser);
        end 
        
        function ret_signal = move_x_mm(  dis_mm, dir, ser)
            MOVE_X = 4;
            serial_string = strcat(num2str(MOVE_X),",",num2str(dis_mm),",",num2str(dir));
            ret_signal = serial_communication(ser, serial_string);
            flush(ser);
        end
        
        function ret_mm = get_distance_from_start(  ser)
            GET_CURRENT_POSITION = 14;
            serial_string = strcat(num2str(GET_CURRENT_POSITION),",0,1");
            %ret_mm = serial_communication(s, serial_string);
            write(ser, serial_string);
            ret_mm = read(ser);
            flush(ser);
        end 
        
        function ret_signal = set_current_position(  pos,ser)
            SET_CURRENT_POS = 6;
            serial_string = strcat(num2str(SET_CURRENT_POS),",",num2str(pos),",0");
            %ret_signal = serial_communication(s, serial_string);
            write(ser, serial_string);
            ret_signal = read(ser);
            flush(ser);
        end
        
        function ret_signal = set_stepsPerRev(  stepsPerRev, ser)
            SET_STEPS_PER_REVOLUTION = 12;
            serial_string = strcat(num2str(SET_STEPS_PER_REVOLUTION),",",num2str(stepsPerRev),",0");
            %ret_signal = serial_communication(s, serial_string);
            write(ser, serial_string);
            ret_signal = read(ser);
            flush(ser);
        end
        
        function ret_signal = set_acceleration(  acceleration, ser)
            SET_ACCELERATION = 10;
            serial_string = strcat(num2str(SET_ACCELERATION),",",num2str(acceleration),",0");
            %ret_signal = serial_communication(s, serial_string);
            write(ser, serial_string);
            ret_signal = read(ser);
            flush(ser);
        end
        
        function ret_signal = set_max_speed(  max_speed,ser)
            SET_MAX_SPEED = 8;
            serial_string = strcat(num2str(SET_MAX_SPEED),",",num2str(max_speed),",0");
            %ret_signal = serial_communication(s, serial_string);
            write(ser, serial_string);
            ret_signal = read(ser);
            flush(ser);
        end
        
        function sig = serial_communication(  ser, message)
            write(ser,message);
            pause(1);
            disp("wait");
            waitfor(s, "NumBytesAvailable");
            sig = read(ser);
        end
        
        function write(  ser, message)
            flush(ser);
            writeline(ser,message);
        end
        
        function out = read(  ser)
            out = readline(ser);
            flush(ser);
        end
%    end
% end