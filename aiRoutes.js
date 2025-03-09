import express from "express";
import { getAIResponse } from "../controllers/aiController.js";

const router = express.Router();
router.post("/analyze", getAIResponse);

export default router;
