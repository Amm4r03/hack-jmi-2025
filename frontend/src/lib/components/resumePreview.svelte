<script>
    export let latexSource = '';
    export let pdfUrl = '';
  
    let activeTab = 'pdf';

    function updatePDFpreview(base64data) {
        pdfUrl = `data:application/pdf; base64, ${base64data}`;
    }
  
    function downloadLatex() {
      const blob = new Blob([latexSource], { type: 'application/x-tex' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'resume.tex';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  
    function downloadPdf() {
      // Assuming the backend provides a direct PDF download URL
      window.open(pdfUrl, '_blank');
    }
  </script>
  
  <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">Resume Preview</h2>
      <div class="space-x-4">
        <button
          class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
          on:click={downloadLatex}
        >
          Download LaTeX
        </button>
        <button
          class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition"
          on:click={downloadPdf}
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
      {#if activeTab === 'pdf'}
        <iframe
          title="PDF Preview"
          src={pdfUrl}
          class="w-full h-full"
        ></iframe>
      {:else}
        <pre class="p-4 bg-gray-50 overflow-auto h-full text-sm font-mono">
          {latexSource}
        </pre>
      {/if}
    </div>
  </div>