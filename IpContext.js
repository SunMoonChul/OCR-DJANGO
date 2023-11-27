import {createContext } from 'react';

const IpContext = createContext({
    ipRas: null,
    setIpRas: () => {},
    ipLap: null,
    setIpLap: () => {},
    ipLoc: null,
    setIpLoc: () => {},
});

export default IpContext;
