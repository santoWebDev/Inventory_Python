import api from "./axios";
export const getLogistics = async (params={}) => (await api.get("/logistics",{params})).data;
export const createLogistics = async (data) => (await api.post("/logistics",data)).data;
export const updateLogistics = async (id,data) => (await api.put(`/logistics/${id}`,data)).data;
