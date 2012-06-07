ArrayList<Particle> getParticles() {
    return particles;
}

ArrayList<Feeling> getFeelings() {
    return feelings;
}

interface JavaScriptInterface {
    void setFromProcessing(String text);
    void setFeeling(String text);
}

JavaScriptInterface js;

void setInterfaceLink (JavaScriptInterface jsin) {
    js = jsin;
}