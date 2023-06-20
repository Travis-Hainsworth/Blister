% classdef Commands_for_Arduino
%    % 
%    % methods
        function ret_mm = return_to_start(obj, s)
            MOVE_TO_START = 2;
            serial_string = strcat(num2str(MOVE_TO_START),",0,1");
            ret_mm = serial_communication(s, serial_string);
            flush(s);
        end 
        
        function ret_signal = move_x_mm(obj, dis_mm, dir, s)
            MOVE_X = 4;
            serial_string = strcat(num2str(MOVE_X),",",num2str(dis_mm),",",num2str(dir));
            ret_signal = serial_communication(s, serial_string);
            flush(s);
        end
        
        function ret_mm = get_distance_from_start(obj, s)
            GET_CURRENT_POSITION = 14;
            serial_string = strcat(num2str(GET_CURRENT_POSITION),",0,1");
            %ret_mm = serial_communication(s, serial_string);
            write(s, serial_string);
            ret_mm = read(s);
            flush(s);
        end 
        
        function ret_signal = set_current_position(obj, pos,s)
            SET_CURRENT_POS = 6;
            serial_string = strcat(num2str(SET_CURRENT_POS),",",num2str(pos),",0");
            %ret_signal = serial_communication(s, serial_string);
            write(s, serial_string);
            ret_signal = read(s);
            flush(s);
        end
        
        function ret_signal = set_stepsPerRev(obj, stepsPerRev, s)
            SET_STEPS_PER_REVOLUTION = 12;
            serial_string = strcat(num2str(SET_STEPS_PER_REVOLUTION),",",num2str(stepsPerRev),",0");
            %ret_signal = serial_communication(s, serial_string);
            write(s, serial_string);
            ret_signal = read(s);
            flush(s);
        end
        
        function ret_signal = set_acceleration(obj, acceleration, s)
            SET_ACCELERATION = 10;
            serial_string = strcat(num2str(SET_ACCELERATION),",",num2str(acceleration),",0");
            %ret_signal = serial_communication(s, serial_string);
            write(s, serial_string);
            ret_signal = read(s);
            flush(s);
        end
        
        function ret_signal = set_max_speed(obj, max_speed,s)
            SET_MAX_SPEED = 8;
            serial_string = strcat(num2str(SET_MAX_SPEED),",",num2str(max_speed),",0");
            %ret_signal = serial_communication(s, serial_string);
            write(s, serial_string);
            ret_signal = read(s);
            flush(s);
        end
        
        function sig = serial_communication(obj, s, message)
            write(s,message);
            pause(1);
            disp("wait");
            waitfor(s, "NumBytesAvailable");
            sig = read(s);
        end
        
        function write(obj, s, message)
            flush(s);
            writeline(s,message);
        end
        
        function out = read(obj, s)
            out = readline(s);
            flush(s);
        end
%    end
% end