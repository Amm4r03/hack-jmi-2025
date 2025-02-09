<script>
    export let latexSource = '';
    export let pdfUrl = '';
    
    let activeTab = 'pdf';
    let pdfData = '';

    // Function to handle the API response
    export function handleAPIResponse(response) {
        if (response.latex_source) {
            latexSource = response.latex_source;
        }
        if (response.pdf_base64) {
            pdfData = `data:application/pdf;base64,${response.pdf_base64}`;
            pdfUrl = pdfData;
        }
    }
  
    function downloadLatex() {
        if (!latexSource) return;
        
        const blob = new Blob([latexSource], { type: 'application/x-tex' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'resume.tex';
        a.click();
        URL.revokeObjectURL(url);
    }
  
    function downloadPdf() {
        if (!pdfData) return;
        
        const byteCharacters = atob(pdfData.split(',')[1]);
        const byteNumbers = new Array(byteCharacters.length);
        
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'application/pdf' });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'resume.pdf';
        a.click();
        URL.revokeObjectURL(url);
    }
</script>

<div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
    <div class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-bold">Resume Preview</h2>
        <div class="space-x-4">
            <button
                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
                on:click={downloadLatex}
                disabled={!latexSource}
            >
                Download LaTeX
            </button>
            <button
                class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition"
                on:click={downloadPdf}
                disabled={!pdfData}
            >
                Download PDF
            </button>
        </div>
    </div>

    <div class="border-b border-gray-200 mb-4">
        <nav class="flex space-x-4">
            <button
                class={`py-2 px-4 ${activeTab === 'pdf' ? 'border-b-2 border-blue-500 text-blue-500' : 'text-gray-500'}`}
                on:click={() => activeTab = 'pdf'}
            >
                PDF Preview
            </button>
            <button
                class={`py-2 px-4 ${activeTab === 'latex' ? 'border-b-2 border-blue-500 text-blue-500' : 'text-gray-500'}`}
                on:click={() => activeTab = 'latex'}
            >
                LaTeX Source
            </button>
        </nav>
    </div>

    <div class="preview-container h-[600px] border rounded-lg">
        {#if activeTab === 'pdf' && pdfData}
            <embed
                src={pdfData}
                type="application/pdf"
                class="w-full h-full"
            />
        {:else if activeTab === 'latex'}
            <pre class="p-4 bg-gray-50 overflow-auto h-full text-sm font-mono">
                {latexSource}
            </pre>
        {:else}
            <div class="flex items-center justify-center h-full text-gray-500">
                No preview available
            </div>
        {/if}
    </div>
</div>