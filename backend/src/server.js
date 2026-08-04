require('dotenv').config();
const app =require("./app")
const PORT=8000;
console.log(PORT);

app.listen(PORT,()=>{
    console.log(`Server started on port ${PORT}`);
})