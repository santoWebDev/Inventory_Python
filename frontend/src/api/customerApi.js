import api from "./axios";
export const getCustomers = async (params={}) => (await api.get("/customers",{params})).data;
export const createCustomer = async (data) => (await api.post("/customers",data)).data;
export const updateCustomer = async (id,data) => (await api.put(`/customers/${id}`,data)).data;
export const deleteCustomer = async (id) => (await api.delete(`/customers/${id}`)).data;
