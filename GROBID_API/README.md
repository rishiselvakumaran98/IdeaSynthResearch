# How to run GROBID_API

## Step 1: Set Up GROBID

### Option 1: Run GROBID via Docker (Recommended)

1. **Install Docker**: Ensure Docker is installed on your system. You can download it from [Docker's official website](https://www.docker.com/get-started).

2. **Pull the GROBID Docker Image from terminal**:

   ```bash
   docker pull lfoppiano/grobid:0.8.2
   ```


3. **Run the GROBID Container**:

   ```bash
   docker run --rm --init --ulimit core=0 -p 8070:8070 lfoppiano/grobid:0.8.2
   ```



This command starts the GROBID service, making it accessible at `http://localhost:8070`.

### Option 2: Run GROBID Locally Without Docker

If you prefer not to use Docker, you can build and run GROBID locally:

1. **Clone the GROBID Repository**:

   ```bash
   git clone https://github.com/kermitt2/grobid.git
   cd grobid
   ```



2. **Build and Run GROBID**:

   ```bash
   ./gradlew run
   ```



This will start the GROBID service on `http://localhost:8070`.

For more detailed instructions, refer to the [GROBID Documentation](https://grobid.readthedocs.io/en/latest/Grobid-service/).

---

## Step 2: Prepare Your PDF

Ensure your research paper is saved locally. For this example, we'll assume the file is named `IdeaSynth_Research_paper.pdf` and is located in the same directory as your Python script.

---

## Step 3: Process the PDF using the API requests below

Certainly! Below is the continuation and completion of the GROBID API documentation for endpoints 18 through 31, focusing on their usage with a PDF like `KnownNet_Research_Paper.pdf`.

---

## 📄 GROBID API Endpoint Documentation (Continued)

### 18. **`POST /api/processCitationPatentTXT`**

* **Purpose**: Processes patent citations from plain text files.([GROBID][1])

* **Input**:

  * Plain text file (`multipart/form-data`)

* **Output**: TEI XML with structured patent citation data.([Stack Overflow][2])

* **Example**:

```bash
  curl -X POST -F input=@patent.txt "http://localhost:8070/api/processCitationPatentTXT" --output processCitations.tei.xml
```



---

### 19. **`POST /api/processDate`**

* **Purpose**: Parses a raw date string into structured TEI XML.([GROBID][3])

* **Input**:

  * Date string (`text/plain`)

* **Output**: TEI XML with structured date information.

* **Example**:

```bash
  curl -X POST --data "March 15, 2021" "http://localhost:8070/api/processDate" --output processDate.tei.xml
```



---

### 20. **`PUT /api/processDate`**

* **Purpose**: Same as POST `/api/processDate`.

* **Input**: Same as above.([GROBID][4])

* **Output**: Same as above.

---

### 21. **`POST /api/processFulltextAssetDocument`**

* **Purpose**: Processes the full text of a PDF, including assets like figures and tables, into structured TEI XML.

* **Input**:

  * PDF file (`multipart/form-data`)
  * Optional parameters:

    * `segmentSentences` (boolean): Segment text into sentences.
    * `teiCoordinates` (string): Include coordinates for specified elements (e.g., `ref`, `figure`).

* **Output**: TEI XML with structured full text and asset information.

* **Example**:

```bash
  curl -X POST -F input=@KnownNet_Research_Paper.pdf -F segmentSentences=1 -F teiCoordinates=ref -F teiCoordinates=figure "http://localhost:8070/api/processFulltextAssetDocument" --output processFullTextAsset.tei.xml
```



---

### 22. **`PUT /api/processFulltextAssetDocument`**

* **Purpose**: Same as POST `/api/processFulltextAssetDocument`.([GitHub][5])

* **Input**: Same as above.([GROBID][6])

* **Output**: Same as above.

---

### 23. **`POST /api/processFulltextDocument`**

* **Purpose**: Processes the full text of a PDF into structured TEI XML.

* **Input**:

  * PDF file (`multipart/form-data`)
  * Optional parameters:

    * `consolidateHeader` (string): Consolidate header metadata (`0`, `1`, `2`, or `3`).
    * `consolidateCitations` (boolean): Consolidate citation metadata.
    * `segmentSentences` (boolean): Segment text into sentences.
    * `teiCoordinates` (string): Include coordinates for specified elements.

* **Output**: TEI XML with structured full text.([GROBID][7])

* **Example**:

```bash
  curl -X POST -F input=@KnownNet_Research_Paper.pdf -F consolidateHeader=1 -F consolidateCitations=1 -F segmentSentences=1 -F teiCoordinates=ref -F teiCoordinates=figure "http://localhost:8070/api/processFulltextDocument"
```



---

### 24. **`PUT /api/processFulltextDocument`**

* **Purpose**: Same as POST `/api/processFulltextDocument`.

* **Input**: Same as above.

* **Output**: Same as above.([GitHub][8])

---

### 25. **`POST /api/processFundingAcknowledgement`**

* **Purpose**: Extracts funding and acknowledgment information from a PDF.

* **Input**:

  * PDF file (`multipart/form-data`)

* **Output**: TEI XML with structured funding and acknowledgment data.([GROBID][9])

* **Example**:

```bash
  curl -X POST -F input=@KnownNet_Research_Paper.pdf "http://localhost:8070/api/processFundingAcknowledgement"
```



---

### 26. **`POST /api/processHeaderDocument`**

* **Purpose**: Extracts the header (title, authors, affiliations, etc.) from a PDF into structured TEI XML or BibTeX.([GROBID][4])

* **Input**:

  * PDF file (`multipart/form-data`)
  * Optional parameters:

    * `consolidateHeader` (string): Consolidate header metadata (`0`, `1`, `2`, or `3`).
    * `includeRawAffiliations` (boolean): Include raw affiliation strings.
    * `includeRawCopyrights` (boolean): Include raw copyright/license strings.
    * `start` (integer): Start page number.
    * `end` (integer): End page number.

* **Output**: TEI XML or BibTeX with structured header information.

* **Example**:

```bash
  curl -X POST -F input=@KnownNet_Research_Paper.pdf -F consolidateHeader=1 -F includeRawAffiliations=1 -F includeRawCopyrights=1 -F start=1 -F end=2 "http://localhost:8070/api/processHeaderDocument" --output HeaderDocument.tei.xml
```



---

### 27. **`PUT /api/processHeaderDocument`**

* **Purpose**: Same as POST `/api/processHeaderDocument`.

* **Input**: Same as above.([GitHub][10])

* **Output**: Same as above.

---

### 28. **`POST /api/processHeaderFundingDocument`**

* **Purpose**: Extracts funding information from the header section of a PDF.

* **Input**:

  * PDF file (`multipart/form-data`)([GitHub][11])

* **Output**: TEI XML with structured funding information.([GROBID][9])

* **Example**:

```bash
  curl -X POST -F input=@KnownNet_Research_Paper.pdf "http://localhost:8070/api/processHeaderFundingDocument" --output HeaderFunding.tei.xml
```



---

### 29. **`POST /api/processHeaderNames`**

* **Purpose**: Parses author names from the header section into structured TEI XML.

* **Input**:

  * Raw author names string (`text/plain`)

* **Output**: TEI XML with structured author name data.

* **Example**:

```bash
  curl -X POST --data "John Smith; Alice Johnson" "http://localhost:8070/api/processHeaderNames" --output HeaderName.tei.xml
```



---

### 30. **`PUT /api/processHeaderNames`**

* **Purpose**: Same as POST `/api/processHeaderNames`.([LangChain Python API][12])

* **Input**: Same as above.

* **Output**: Same as above.([GROBID][3])

---

### 31. **`POST /api/processReferences`**

* **Purpose**: Extracts and parses the references section from a PDF into structured TEI XML.

* **Input**:

  * PDF file (`multipart/form-data`)
  * Optional parameters:

    * `consolidateCitations` (boolean): Consolidate citation metadata.

* **Output**: TEI XML with structured references.([GROBID][7], [GROBID][3])

* **Example**:

```bash
  curl -X POST -F input=@KnownNet_Research_Paper.pdf -F consolidateCitations=1 "http://localhost:8070/api/processReferences" --output KnownNet_Research_Paper.tei.xml
```

Certainly! Below is the continuation and completion of the GROBID API documentation for endpoints 18 through 31, focusing on their usage with a PDF like `KnownNet_Research_Paper.pdf`.

---

## 📄 GROBID API Endpoint Documentation (Continued)

### 18. **`POST /api/processCitationPatentTXT`**

* **Purpose**: Processes patent citations from plain text files.([GROBID][1])

* **Input**:

  * Plain text file (`multipart/form-data`)

* **Output**: TEI XML with structured patent citation data.([Stack Overflow][2])

* **Example**:

```bash
  curl -X POST -F input=@patent.txt "http://localhost:8070/api/processCitationPatentTXT"
```



---

### 19. **`POST /api/processDate`**

* **Purpose**: Parses a raw date string into structured TEI XML.

* **Input**:

  * Date string (`text/plain`)

* **Output**: TEI XML with structured date information.

* **Example**:

```bash
  curl -X POST --data "March 15, 2021" "http://localhost:8070/api/processDate" --output ProcessedDate.tei.xml
```



---

### 20. **`PUT /api/processDate`**

* **Purpose**: Same as POST `/api/processDate`.

* **Input**: Same as above.

* **Output**: Same as above.

---

### 21. **`POST /api/processFulltextAssetDocument`**

* **Purpose**: Processes the full text of a PDF, including assets like figures and tables, into structured TEI XML.

* **Input**:

  * PDF file (`multipart/form-data`)
  * Optional parameters:

    * `segmentSentences` (boolean): Segment text into sentences.
    * `teiCoordinates` (string): Include coordinates for specified elements (e.g., `ref`, `figure`).

* **Output**: TEI XML with structured full text and asset information.

* **Example**:

```bash
  curl -X POST -F input=@KnownNet_Research_Paper.pdf -F segmentSentences=1 -F teiCoordinates=ref -F teiCoordinates=figure "http://localhost:8070/api/processFulltextAssetDocument" --output KnownNet_Research_Paper.tei.xml
```



---

### 22. **`PUT /api/processFulltextAssetDocument`**

* **Purpose**: Same as POST `/api/processFulltextAssetDocument`.

* **Input**: Same as above.

* **Output**: Same as above.

---

### 23. **`POST /api/processFulltextDocument`**

* **Purpose**: Processes the full text of a PDF into structured TEI XML.

* **Input**:

  * PDF file (`multipart/form-data`)
  * Optional parameters:

    * `consolidateHeader` (string): Consolidate header metadata (`0`, `1`, `2`, or `3`).
    * `consolidateCitations` (boolean): Consolidate citation metadata.
    * `segmentSentences` (boolean): Segment text into sentences.
    * `teiCoordinates` (string): Include coordinates for specified elements.

* **Output**: TEI XML with structured full text.

* **Example**:

```bash
  curl -X POST -F input=@KnownNet_Research_Paper.pdf -F consolidateHeader=1 -F consolidateCitations=1 -F segmentSentences=1 -F teiCoordinates=ref -F teiCoordinates=figure "http://localhost:8070/api/processFulltextDocument" --output KnownNet_Research_Paper.tei.xml
```



---

### 24. **`PUT /api/processFulltextDocument`**

* **Purpose**: Same as POST `/api/processFulltextDocument`.

* **Input**: Same as above.

* **Output**: Same as above.

---

### 25. **`POST /api/processFundingAcknowledgement`**

* **Purpose**: Extracts funding and acknowledgment information from a PDF.

* **Input**:

  * PDF file (`multipart/form-data`)

* **Output**: TEI XML with structured funding and acknowledgment data.

* **Example**:

```bash
  curl -X POST -F input=@KnownNet_Research_Paper.pdf "http://localhost:8070/api/processFundingAcknowledgement" --output KnownNet_Research_Paper.tei.xml
```



---

### 26. **`POST /api/processHeaderDocument`**

* **Purpose**: Extracts the header (title, authors, affiliations, etc.) from a PDF into structured TEI XML or BibTeX.([GROBID][4])

* **Input**:

  * PDF file (`multipart/form-data`)
  * Optional parameters:

    * `consolidateHeader` (string): Consolidate header metadata (`0`, `1`, `2`, or `3`).
    * `includeRawAffiliations` (boolean): Include raw affiliation strings.
    * `includeRawCopyrights` (boolean): Include raw copyright/license strings.
    * `start` (integer): Start page number.
    * `end` (integer): End page number.

* **Output**: TEI XML or BibTeX with structured header information.

* **Example**:

```bash
  curl -X POST -F input=@KnownNet_Research_Paper.pdf -F consolidateHeader=1 -F includeRawAffiliations=1 -F includeRawCopyrights=1 -F start=1 -F end=2 "http://localhost:8070/api/processHeaderDocument" --output KnownNet_Research_Paper.tei.xml
```



---

### 27. **`PUT /api/processHeaderDocument`**

* **Purpose**: Same as POST `/api/processHeaderDocument`.

* **Input**: Same as above.

* **Output**: Same as above.

---

### 28. **`POST /api/processHeaderFundingDocument`**

* **Purpose**: Extracts funding information from the header section of a PDF.

* **Input**:

  * PDF file (`multipart/form-data`)

* **Output**: TEI XML with structured funding information.

* **Example**:

```bash
  curl -X POST -F input=@KnownNet_Research_Paper.pdf "http://localhost:8070/api/processHeaderFundingDocument" --output KnownNet_Research_Paper.tei.xml
```



---

### 29. **`POST /api/processHeaderNames`**

* **Purpose**: Parses author names from the header section into structured TEI XML.

* **Input**:

  * Raw author names string (`text/plain`)

* **Output**: TEI XML with structured author name data.

* **Example**:

```bash
  curl -X POST --data "John Smith; Alice Johnson" "http://localhost:8070/api/processHeaderNames" --output HeaderNames.tei.xml
```


---

### 30. **`PUT /api/processHeaderNames`**

* **Purpose**: Same as POST `/api/processHeaderNames`.

* **Input**: Same as above.

* **Output**: Same as above. 

---

### 31. **`POST /api/processReferences`**

* **Purpose**: Extracts and parses the references section from a PDF into structured TEI XML.

* **Input**:

  * PDF file (`multipart/form-data`)
  * Optional parameters:

    * `consolidateCitations` (boolean): Consolidate citation metadata.

* **Output**: TEI XML with structured references.

* **Example**:

```bash
  curl -X POST -F input=@KnownNet_Research_Paper.pdf -F consolidateCitations=1 "http://localhost:8070/api/processReferences" --output KnownNet_Research_Paper.tei.xml
```

---
