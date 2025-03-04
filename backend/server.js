import express from 'express';
import dotenv from 'dotenv';
import {connectDB} from "./config/db.js";

dotenv.config();


const app = express();
app.post("/api/products", async (req, res)=>{

  const product = req.body; // user body will send this data
  
  if(!product.name || !product.price){
    return res.status(400).json({success:false,messasge:"please provid all fields  "});
   }
        const newProduct = new Product(product);

        try{
          await newProduct.save();
        res.status(201).json({success:true , data:newProduct});
        } catch (error){
        console.error("Error in  Create Product:", error.messasge);
          res.status(500).json({success:false, messasge:"Server Error"});
        };
       });
        
console.log(process.env.MONGO_URI);

app.listen(5000,()=>{
  connectDB();
  console.log("Server started at http://localhost:5000");

});

