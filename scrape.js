const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function getFinalUrl(url) {
    try {
        const response = await axios.get(url, { maxRedirects: 0, validateStatus: null });
        if (response.status >= 300 && response.status < 400 && response.headers.location) {
            return response.headers.location;
        }
        return url;
    } catch (error) {
        console.error(`Failed to get final URL for ${url}:`, error.message);
        return null;
    }
}

async function parsePage(url) {
    const finalUrl = await getFinalUrl(url);
    if (!finalUrl) return [];

    try {
        const response = await axios.get(finalUrl);
        const $ = cheerio.load(response.data);

        const companyData = [];

        $('table.ts1 tr').each((index, element) => {
            if (index === 0) return; // Skip the header row
            const columns = $(element).find('td');
            if (columns.length > 1) {
