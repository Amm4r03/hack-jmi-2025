<script>
    import ResumeForm from '$lib/components/ResumeForm.svelte';
    import ResumePreview from '$lib/components/ResumePreview.svelte';
    
    let showPreview = false;
    let previewData = {
      latexSource: '',
      pdfUrl: ''
    };
  
    function handleResumeGenerated(event) {
      previewData = event.detail;
      showPreview = true;
    }
  </script>
  
  <main class="min-h-screen bg-gray-100 py-8">
    <div class="container mx-auto px-4">
      <header class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">LaTeX Resume Builder</h1>
        <p class="text-gray-600">Create professional resumes with LaTeX templates</p>
      </header>
  
      {#if !showPreview}
        <ResumeForm on:resumeGenerated={handleResumeGenerated} />
      {:else}
        <div class="mb-4">
          <button
            class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 transition hover:cursor-pointer"
            on:click={() => showPreview = false}
          >
            Back to form
          </button>
        </div>
        <ResumePreview
          latexSource={previewData.latexSource}
          pdfUrl={previewData.pdfUrl}
        />
      {/if}
    </div>
  </main>