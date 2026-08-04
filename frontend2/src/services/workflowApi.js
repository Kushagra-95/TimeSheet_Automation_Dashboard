// import axios from "axios";

// const API = axios.create({
//     baseURL: "http://localhost:8000/api",
// });

// export const runWorkflow = async () => {
//     const response = await API.post("/workflow/run");
//     return response.data;
// };

// export const downloadFile = async (filename) => {
//   const response = await API.get(`/files/download/${encodeURIComponent(filename)}`, {
//     responseType: "blob",
//   });

//   return response.data;
// };

// export const downloadFolder = async (folderName) => {
//   const response = await API.get(`/folders/download/${encodeURIComponent(folderName)}`,{
//       responseType: "blob",
//     }
//   );

//   return response.data;
// };
// export const uploadFile = async (file) => {
//   const formData = new FormData();
//   formData.append("file", file);

//   const response = await API.post("/upload", formData, {
//     headers: {
//       "Content-Type": "multipart/form-data",
//     },
//   });

//   return response.data;
// };

import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await API.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const runWorkflow = async (jobId) => {
  const response = await API.post("/workflow/run", {
    jobId,
  });

  return response.data;
};

export const downloadFile = async (filename, jobId) => {
  const response = await API.get(
    `/files/download/${encodeURIComponent(filename)}?jobId=${jobId}`,
    {
      responseType: "blob",
    }
  );

  return response.data;
};

export const downloadFolder = async (folderName, jobId) => {
  const response = await API.get(
    `/folders/download/${encodeURIComponent(folderName)}?jobId=${jobId}`,
    {
      responseType: "blob",
    }
  );

  return response.data;
};