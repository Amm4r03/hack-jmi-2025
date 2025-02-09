<script>
    import ResumeForm from '$lib/components/ResumeForm.svelte';
    import ResumePreview from '$lib/components/ResumePreview.svelte';
    import { onMount } from 'svelte';

    let showPreview = false;
    let previewComponent;
    let error = null;

    function handleResumeGenerated(event) {
        error = null;
        showPreview = true; // Immediately show the preview
        
        // Pass the initial form data to the preview component
        if (previewComponent) {
            previewComponent.handleAPIResponse({ status: "processing" });
        }

        // Start generating the resume in the background
        fetch('http://localhost:5000/generate-resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(event.detail)
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                throw new Error(result.error);
            }

            // Update the preview component when the PDF is ready
            if (previewComponent) {
                previewComponent.handleAPIResponse(result);
            }
        })
        .catch(err => {
            console.error('Error generating resume:', err);
            error = err.message || 'Failed to generate resume';
        });
    }
</script>

<main class="min-h-screen bg-gray-100 py-8">
    <div class="container mx-auto px-4">
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-gray-800 mb-2">LaTeX Resume Builder</h1>
            <p class="text-gray-600">Create professional resumes with LaTeX templates</p>
        </header>

        {#if error}
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
                <strong class="font-bold">Error!</strong>
                <span class="block sm:inline"> {error}</span>
            </div>
        {/if}

        {#if !showPreview}
            <ResumeForm on:resumeGenerated={handleResumeGenerated} />
        {:else}
            <div class="mb-4">
                <button
                    class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 transition hover:cursor-pointer"
                    on:click={() => {
                        showPreview = false;
                        error = null;
                    }}
                >
                    Back to form
                </button>
            </div>
            <ResumePreview bind:this={previewComponent} />
        {/if}
    </div>
</main>
