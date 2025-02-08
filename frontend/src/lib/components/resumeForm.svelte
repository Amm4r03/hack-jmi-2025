<script>
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
    
    let formData = {
      name: '',
      email: '',
      phone: '',
      location: '',
      linkedin: '',
      github: '',
      experience: [{ company: '', title: '', date: '', location: '', description: '' }],
      education: [{ school: '', degree: '', date: '', location: '' }],
      projects: [{ name: '', description: '', technologies: '' }],
      skills: ''
    };
  
    function addExperience() {
      formData.experience = [...formData.experience, { company: '', title: '', date: '', location: '', description: '' }];
    }
  
    function removeExperience(index) {
      formData.experience = formData.experience.filter((_, i) => i !== index);
    }

    function addEducation() {
      formData.education = [...formData.education, { school: '', degree: '', date: '', location: '' }];
    }

    function removeEducation(index) {
      formData.education = formData.education.filter((_, i) => i !== index);
    }

    function addProject() {
      formData.projects = [...formData.projects, { name: '', description: '', technologies: '' }];
    }

    function removeProject(index) {
      formData.projects = formData.projects.filter((_, i) => i !== index);
    }
  
    async function handleSubmit() {
      try {
        const response = await fetch('http://127.0.0.1:5000/generate-resume', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });
        
        const data = await response.json();
        dispatch('resumeGenerated', data);
      } catch (error) {
        console.error('Error generating resume:', error);
      }
    }
</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-6 max-w-4xl mx-auto p-6">
    <div class="space-y-4">
        <h2 class="text-2xl font-bold">Personal Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
                type="text"
                bind:value={formData.name}
                placeholder="Full Name"
                class="w-full p-2 border rounded"
                required
            />
            <input
                type="email"
                bind:value={formData.email}
                placeholder="Email"
                class="w-full p-2 border rounded"
                required
            />
            <input
                type="tel"
                bind:value={formData.phone}
                placeholder="Phone"
                class="w-full p-2 border rounded"
            />
            <input
                type="text"
                bind:value={formData.location}
                placeholder="Location"
                class="w-full p-2 border rounded"
            />
            <input
                type="text"
                bind:value={formData.linkedin}
                placeholder="LinkedIn Username"
                class="w-full p-2 border rounded"
            />
            <input
                type="text"
                bind:value={formData.github}
                placeholder="GitHub Username"
                class="w-full p-2 border rounded"
            />
        </div>
    </div>

    <!-- Experience Section -->
    <div class="space-y-4">
        <div class="flex justify-between items-center">
            <h2 class="text-2xl font-bold">Experience</h2>
            <button
                type="button"
                on:click={addExperience}
                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 hover:cursor-pointer"
            >
                Add Experience
            </button>
        </div>
        
        {#each formData.experience as exp, i}
            <div class="space-y-4 p-4 border rounded">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input
                        type="text"
                        bind:value={exp.company}
                        placeholder="Company"
                        class="w-full p-2 border rounded"
                    />
                    <input
                        type="text"
                        bind:value={exp.title}
                        placeholder="Title"
                        class="w-full p-2 border rounded"
                    />
                    <input
                        type="text"
                        bind:value={exp.date}
                        placeholder="Date Range"
                        class="w-full p-2 border rounded"
                    />
                    <input
                        type="text"
                        bind:value={exp.location}
                        placeholder="Location"
                        class="w-full p-2 border rounded"
                    />
                </div>
                <textarea
                    bind:value={exp.description}
                    placeholder="Description"
                    class="w-full p-2 border rounded h-32"
                ></textarea>
                {#if i > 0}
                    <button
                        type="button"
                        on:click={() => removeExperience(i)}
                        class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600  hover:cursor-pointer"
                    >
                        Remove
                    </button>
                {/if}
            </div>
        {/each}
    </div>

    <!-- Education Section -->
    <div class="space-y-4">
        <div class="flex justify-between items-center">
            <h2 class="text-2xl font-bold">Education</h2>
            <button
                type="button"
                on:click={addEducation}
                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600  hover:cursor-pointer"
            >
                Add Education
            </button>
        </div>
        
        {#each formData.education as edu, i}
            <div class="space-y-4 p-4 border rounded">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input
                        type="text"
                        bind:value={edu.school}
                        placeholder="School"
                        class="w-full p-2 border rounded"
                    />
                    <input
                        type="text"
                        bind:value={edu.degree}
                        placeholder="Degree"
                        class="w-full p-2 border rounded"
                    />
                    <input
                        type="text"
                        bind:value={edu.date}
                        placeholder="Date Range"
                        class="w-full p-2 border rounded"
                    />
                    <input
                        type="text"
                        bind:value={edu.location}
                        placeholder="Location"
                        class="w-full p-2 border rounded"
                    />
                </div>
                {#if i > 0}
                    <button
                        type="button"
                        on:click={() => removeEducation(i)}
                        class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 hover:cursor-pointer"
                    >
                        Remove
                    </button>
                {/if}
            </div>
        {/each}
    </div>

    <!-- Projects Section -->
    <div class="space-y-4">
        <div class="flex justify-between items-center">
            <h2 class="text-2xl font-bold">Projects</h2>
            <button
                type="button"
                on:click={addProject}
                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 hover:cursor-pointer"
            >
                Add Project
            </button>
        </div>
        
        {#each formData.projects as project, i}
            <div class="space-y-4 p-4 border rounded">
                <div class="grid grid-cols-1 gap-4">
                    <input
                        type="text"
                        bind:value={project.name}
                        placeholder="Project Name"
                        class="w-full p-2 border rounded"
                    />
                    <textarea
                        bind:value={project.description}
                        placeholder="Project Description"
                        class="w-full p-2 border rounded h-32"
                    ></textarea>
                    <input
                        type="text"
                        bind:value={project.technologies}
                        placeholder="Technologies Used (comma-separated)"
                        class="w-full p-2 border rounded"
                    />
                </div>
                {#if i > 0}
                    <button
                        type="button"
                        on:click={() => removeProject(i)}
                        class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600  hover:cursor-pointer"
                    >
                        Remove
                    </button>
                {/if}
            </div>
        {/each}
    </div>

    <!-- Skills Section -->
    <div class="space-y-4">
        <h2 class="text-2xl font-bold">Skills</h2>
        <textarea
            bind:value={formData.skills}
            placeholder="Enter your skills (comma-separated)"
            class="w-full p-2 border rounded h-32"
        ></textarea>
    </div>

    <!-- Submit Button -->
    <div class="flex justify-end">
        <button
            type="submit"
            class="bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600 font-semibold hover:cursor-pointer"
        >
            Generate Resume
        </button>
    </div>
</form>