// A class to describe a group of Particles
// An ArrayList is used to manage the list of Particles 

class ParticleSystem {

  ArrayList particles;    // An arraylist for all the particles
  PVector origin;        // An origin point for where particles are born

  ParticleSystem(int num, PVector v) {
    particles = new ArrayList();              // Initialize the arraylist
    origin = v.get();                        // Store the origin point
    //for (int i = 0; i < num; i++) {
    //  particles.add(new Particle(origin));    // Add "num" amount of particles to the arraylist
    //}
  }

  void run() {
    // Cycle through the ArrayList backwards b/c we are deleting
    alreadyShowing = false;
    for (int i = particles.size()-1; i >= 0; i--) {
      Particle p = (Particle) particles.get(i);
      p.run();
      //if (p.dead()) {
      //  particles.remove(i);
      //}
    }
  }

  void addParticle(Tweet tweet) {
    particles.add(new Particle(origin, tweet));
  }
  
  void addParticle(float x, float y, Tweet tweet) {
    particles.add(new Particle(new PVector(x,y), tweet));
  }

}
