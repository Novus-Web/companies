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
            if (columns.length > 1) { // Ensure it's not an empty row
                const companyName = $(columns[0]).text().trim();
                const companyLink = $(columns[0]).find('a').attr('href');
                companyData.push({ name: companyName, link: companyLink });
            }
        });

        return companyData;
    } catch (error) {
        console.error(`Failed to parse page ${finalUrl}:`, error.message);
        return [];
    }
}

async function scrapeAllPages() {
    const baseUrl = "https://www.listafirme.ro/hunedoara/petrosani/";
    const allCompanyDetails = [];
    for (let pageNumber = 1; pageNumber <= 1; pageNumber++) {  // Adjust range as needed
        const pageUrl = `${baseUrl}o${pageNumber}.htm`;
        console.log(`Scraping page: ${pageUrl}`);
        const companyDetails = await parsePage(pageUrl);
        allCompanyDetails.push(...companyDetails);
    }
    return allCompanyDetails;
}

async function saveToJson(data, filename) {
    fs.writeFileSync(filename, JSON.stringify(data, null, 4), 'utf-8');
}

(async () => {
    const allCompanyDetails = await scrapeAllPages();
    await saveToJson(allCompanyDetails, 'company_data.json');
    console.log('Data saved to company_data.json');
})();
