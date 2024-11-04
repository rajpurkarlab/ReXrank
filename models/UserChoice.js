const mongoose = require('mongoose');

const UserChoiceSchema = new mongoose.Schema({
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    imageId: { type: String, required: true },
    choice: { type: String, required: true }
  }, { timestamps: true });
  
module.exports = mongoose.model('UserChoice', UserChoiceSchema);