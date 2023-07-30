function [auores alores buores blores del buf] = rtcgpc(aui, ali, bui, bli, ed)
% RTCGPC   Compute the output of a greedy processing component.
%    [AU',AL',BU',BL',Del,Buf] = RTCGPC(AU,AL,BU,BL,ED) computes the output 
%    curves of a greedy processing component that processes a discrete 
%    event stream with upper arrival curve AU and lower arrival curve 
%    AL on a resource with upper service curve BU and lower
%    service curve BL. The parameter ED specifies the 
%    execution demand of the events on the input
%    event stream. RTCGPC returns four curves [AU',AL',BU',BL'],
%    that model the outgoing event stream with the upper 
%    arrival curve AU' and the lower arrival curve AL', and
%    the remaining resources with the upper service curve BU'
%    and the lower service curve BL'.
%    The execution demand can be a scalar: In this case we have
%    WCED = BCED (worst case execution demand = best case execution
%    demand). Otherwise, ED = [WCED BCED].
%    Del and Buf are the worst-case delay and buffer space requirement
%    associated to the input stream.
%
%    [AU',AL',BU',BL',Del,Buf] = RTCGPC(AU,AL,BU,BL) computes the output of a 
%    greedy processing component, where the execution 
%    demand of the events is set to 1.
%
%    [A',B',Del,Buf] = RTCGPC(A,B,ED) computes the output of a greedy processing 
%    component that processes an event stream with arrival curve set A, 
%    service curve set B and execution demand ED.
%
%    [A',B',Del,Buf] = RTCGPC(A,B) computes the output of a greedy processing 
%    component that processes an event stream with arrival curve set A, 
%    service curve set B, where the execution demand of the 
%    events is set to 1.
%
%    A greedy processing component is triggered by the events of an
%    incoming event stream. A fully preemptable task is instantiated at
%    every event arrival to process the incoming event, and active tasks
%    are processed in a greedy fashion in FIFO order, while being
%    restricted by the availbility of resources.
%
%    See also RTCPLOTGPC, RTCGSC, RTCDEL, RTCBUF, RTCEDF

%    Author(s): E. Wandeler
%    Copyright 2004-2006 Computer Engineering and Networks Laboratory (TIK) 
%    ETH Zurich, Switzerland.
%    All rights reserved.

if nargin < 2
    error('RTCGPC - too few arguments.')
elseif nargin < 4 % RTCGPC(A,B) or RTCGPC(A,B,ED)
    if (strcmp(class(aui),'ch.ethz.rtc.kernel.Curve[]') && strcmp(class(ali),'ch.ethz.rtc.kernel.Curve[]'))
        if nargin == 2 % RTCGPC(A,B)
            wced = 1; bced = 1;
        else % RTCGPC(A,B,ED)
            if(isscalar(bui))
               wced = bui; bced = bui;
            else
               wced = bui(1);
               bced = bui(2);
            end
        end
        ai = aui;
        bi = ali;
        aui = ai(1);
        ali = ai(2);
        bui = bi(1);
        bli = bi(2);
    else
    	error('RTCGPC - gpc is not defined for the passed argument list.')
    end
elseif nargin == 4 % RTCGPC(AU,AL,BU,BL)
    wced = 1; bced = 1;
elseif nargin == 5 % RTCGPC(AU,AL,BU,BL,ED)
    if(isscalar(ed))
       wced = ed; bced = ed;
    else
       wced = ed(1);
       bced = ed(2);
    end
elseif nargin > 5
    error('RTCGPC - too many arguments.')
end

%aui = rtctimes(aui, wced);
%ali = rtctimes(ali,bced);

%auo = rtcceil(rtcrdivide(rtcmin(rtcmindeconv(rtcminconv(aui, bui), bli), bui), bced));
%alo = rtcfloor(rtcrdivide(rtcmin(rtcminconv(rtcmindeconv(ali, bui), bli), bli), wced));

buo = rtcmaxdeconv(rtcminus(bui, rtctimes(ali, bced)), 0);
blo = rtcmaxconv(rtcminus(bli, rtctimes(aui, wced)), 0);

bui = rtcrdivide(bui, bced);
bli = rtcrdivide(bli, wced);

auo = rtcceil(rtcmin(rtcmindeconv(rtcminconv(aui, bui), bli), bui));
alo = rtcfloor(rtcmin(rtcminconv(rtcmindeconv(ali, bui), bli), bli));

bli = rtcmax(0,rtcfloor(bli));
delay =  rtch(aui, bli);
buffer = rtcv(aui, bli);

if nargin < 4
    auores = [auo alo];
    alores = [buo blo];
    buores = delay;
    blores = buffer;
else
    auores = auo;
    alores = alo;    
    buores = buo;
    blores = blo;
    del = delay;
    buf = buffer;
end