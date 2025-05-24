<!-- Main page component -->
<script lang="ts">
  import { Upload } from 'lucide-svelte';
  import toast from 'svelte-french-toast';
  import VoiceSelector from '$lib/components/VoiceSelector.svelte';
  import AudioRecorder from '$lib/components/AudioRecorder.svelte';
  import { voiceStore, clearSelectedVoice } from '$lib/stores/voices';
  import { onDestroy } from 'svelte';

  let selectedFile: File | null = null;
  let isLoading = false;
  let audioUrl: string | null = null;
  let activeTab: 'upload' | 'record' = 'upload';
  let transformError: string | null = null;

  onDestroy(() => {
    // Clean up any resources
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
    }
    clearSelectedVoice();
  });

  async function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      // Validate file type and size
      if (!file.type.startsWith('audio/')) {
        toast.error('Please select an audio file');
        return;
      }
      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        toast.error('File size must be less than 10MB');
        return;
      }
      selectedFile = file;
      toast.success('File selected successfully');
    }
  }

  async function handleAudioRecorded(blob: Blob) {
    try {
      // Convert webm to wav for better compatibility
      const file = new File([blob], 'recording.wav', { 
        type: 'audio/wav',
        lastModified: Date.now()
      });
      selectedFile = file;
      toast.success('Recording saved successfully!');
    } catch (error) {
      toast.error('Failed to save recording');
      console.error('Recording error:', error);
    }
  }

  function resetState() {
    selectedFile = null;
    audioUrl = null;
    transformError = null;
  }

  async function handleTransform() {
    if (!selectedFile || !$voiceStore.selectedVoice) {
      toast.error('Please select both an audio file and a voice');
      return;
    }

    isLoading = true;
    transformError = null;

    try {
      // Create form data for transformation
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('voice_id', $voiceStore.selectedVoice.id);
      formData.append('retain_prosody', 'true');
      formData.append('retain_accent', 'true');

      console.log('Transforming voice with:', {
        file: selectedFile.name,
        voice: $voiceStore.selectedVoice.name
      });

      // Send transformation request
      const transformResponse = await fetch('http://localhost:8000/api/transform', {
        method: 'POST',
        body: formData
      });

      if (!transformResponse.ok) {
        const errorData = await transformResponse.json().catch(() => ({ detail: transformResponse.statusText }));
        throw new Error(errorData.detail || 'Failed to transform voice');
      }

      const transformData = await transformResponse.json();
      console.log('Voice transformed successfully:', transformData);
      
      // Clean up previous audio URL if it exists
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }

      // Create URL for the transformed audio
      const audioResponse = await fetch(`http://localhost:8000${transformData.url}`);
      if (!audioResponse.ok) {
        throw new Error('Failed to fetch transformed audio');
      }
      
      const audioBlob = await audioResponse.blob();
      audioUrl = URL.createObjectURL(audioBlob);
      
      toast.success('Voice transformation complete!');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
      transformError = errorMessage;
      toast.error(errorMessage);
      console.error('Transform error:', error);
    } finally {
      isLoading = false;
    }
  }

  function handleTabChange(tab: 'upload' | 'record') {
    if (tab !== activeTab) {
      activeTab = tab;
      resetState();
    }
  }
</script>

<main class="container mx-auto px-4 py-8">
  <h1 class="text-4xl font-bold text-center mb-8">VoiceForge</h1>
  
  <div class="max-w-2xl mx-auto">
    <div class="mb-8">
      <VoiceSelector />
    </div>

    <div class="bg-white rounded-lg shadow-md p-6">
      <!-- Tab Navigation -->
      <div class="flex mb-6 border-b">
        <button
          class="px-4 py-2 {activeTab === 'upload' ? 'border-b-2 border-blue-500 text-blue-500' : 'text-gray-500'} transition-colors"
          on:click={() => handleTabChange('upload')}
        >
          Upload File
        </button>
        <button
          class="px-4 py-2 {activeTab === 'record' ? 'border-b-2 border-blue-500 text-blue-500' : 'text-gray-500'} transition-colors"
          on:click={() => handleTabChange('record')}
        >
          Record Audio
        </button>
      </div>

      <!-- Tab Content -->
      {#if activeTab === 'upload'}
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="file">
            Upload Audio File
          </label>
          <div class="flex items-center justify-center w-full">
            <label class="w-full flex flex-col items-center px-4 py-6 bg-white rounded-lg border-2 border-dashed cursor-pointer hover:bg-gray-50 transition-colors">
              <Upload />
              <span class="mt-2 text-base">{selectedFile ? selectedFile.name : 'Select a file'}</span>
              <span class="mt-1 text-sm text-gray-500">Max file size: 10MB</span>
              <input 
                type="file" 
                class="hidden" 
                accept="audio/*"
                on:change={handleFileUpload}
                aria-label="Upload audio file"
              />
            </label>
          </div>
        </div>
      {:else}
        <div class="mb-6">
          <AudioRecorder onAudioRecorded={handleAudioRecorded} />
        </div>
      {/if}

      {#if transformError}
        <div class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {transformError}
        </div>
      {/if}

      <button
        on:click={handleTransform}
        disabled={isLoading || !selectedFile || !$voiceStore.selectedVoice}
        class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {#if isLoading}
          <div class="flex items-center justify-center">
            <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            <span>Processing...</span>
          </div>
        {:else}
          Transform Voice
        {/if}
      </button>

      {#if audioUrl}
        <div class="mt-6">
          <h3 class="text-lg font-semibold mb-2">Transformed Audio</h3>
          <audio 
            controls 
            class="w-full" 
            src={audioUrl}
            on:error={() => toast.error('Failed to load transformed audio')}
          >
            Your browser does not support the audio element.
          </audio>
          <a
            href={audioUrl}
            download="transformed_audio.wav"
            class="mt-4 inline-block text-blue-500 hover:text-blue-600 transition-colors"
          >
            Download Transformed Audio
          </a>
        </div>
      {/if}
    </div>
  </div>
</main>

<style>
  :global(body) {
    background-color: #f3f4f6;
  }
</style> 