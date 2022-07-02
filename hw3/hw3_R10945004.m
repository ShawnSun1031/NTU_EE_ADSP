clear all;
%% 功能設定
score = [1, 1, 5, 5, 6, 6, 5]; % 1: Do, 2: Re, 3: Mi, …..
beat= [ 1, 1, 1, 1, 1, 1, 2]; % 拍子
name= 'twinkle';
rest = [ 1, 0, 0, 0, 0, 0, 0]; % 休止符，若要在某個音調後面加上一個四分休止符則value設為1，若不要休止符則設為0
chord_number = [ 3, 3, 3, 3, 3, 3, 3]; % 設定倍頻的數量 ex: f0、2*f0、3*f0、......
amplitude = [ 1, 1, 1, 1, 1, 1, 1]; % 設定振幅
decay_type = 'linear'; % 可以設定聲音隨 "linear" 衰減， 或者是 "exponential" 衰減
alpha = 0.2 ; % 若設定 "exponential" 衰減，則需要設定 衰減係數 來確定衰減的快慢

getmusic(score, beat, name,rest,chord_number,amplitude,decay_type,alpha)
%% getmusic function
function getmusic(score, beat, name,rest,chord_number,amplitude,decay_type,alpha)
fs = 44100;
for i=1:size(score,2)
    if score(i) == 1
        f(i) = 261.63;
    elseif score(i) == 2
        f(i) = 261.63*2^(2/12);
    elseif score(i) == 3
        f(i) = 261.63*2^(4/12);
    elseif score(i) == 4
        f(i) = 261.63*2^(5/12);
    elseif score(i) == 5
        f(i) = 261.63*2^(7/12);
    elseif score(i) == 6
        f(i) = 261.63*2^(9/12);
    elseif score(i) == 7
        f(i) = 261.63*2^(11/12);
    end
    t(i) = {[0:1/fs:beat(i)-1/fs]};
    if rest(i) == 1
        r(i) = {ones(1,size([0:1/fs:beat(i)-1/fs],2))};
    elseif rest(i) == 0
        r(i) = {0};
    end
end

if decay_type == "linear"
    for i=1:size(amplitude,2)
        m = -(amplitude(i)-0)/t{i}(1,size(t{i},2));
        temp = [];
        for j=1:size(t{i},2)
            temp(j) = amplitude(i) + m*t{i}(1,j);
        end
        A(i) = {temp};
    end
elseif decay_type == "exponential"
    for i=1:size(amplitude,2)
    m = -(amplitude(i)-0)/t{i}(1,size(t{i},2));
    temp = [];
    for j=1:size(t{i},2)
        temp(j) = exp(-alpha*t{i}(1,j));
    end
    A(i) = {amplitude(i)*temp};
    end
end

x = [];
for i=1:size(t,2)
    temp = 0;
    for k=1:chord_number(i)
        temp = temp + sin(2*pi*k*f(i)*t{i});
    end
    x = [x A{i}.*temp];
    if rest(i) == 1;
        x = [x r{i}];
    end
end
filename = [ name '.wav']
sound(x,fs)
audiowrite(filename, x, fs)
end

